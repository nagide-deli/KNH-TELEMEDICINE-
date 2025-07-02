from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import EducationalResource, Question, Answer, Comment
from django.contrib.auth.decorators import login_required


@login_required
def educational_resources_list (request):
    resources = EducationalResource.objects.all()
    resource = resources.first() if resources.exists() else None



    comments = Comment.objects.all()
    questions = Question.objects.all()

    if request.method == "POST":
        resource_id = request.POST.get('resource_id')

        # ✅ Ensure `resource_id` is valid
        if not resource_id:
            messages.error(request, "Invalid resource. Please try again.")
            return render(request, 'educational_resources.html', {'resources': resources, 'resource': resource})

        # ✅ Fetch resource safely
        try:
            resource = EducationalResource.objects.get(id=resource_id)
        except EducationalResource.DoesNotExist:
            messages.error(request, "Resource not found.")
            return render(request, 'educational_resources.html', {'resources': resources, 'resource': resource})

    if request.method == "POST":
        if 'comment_text' in request.POST:  # Posting a comment
            text = request.POST['comment_text']
            resource_id = request.POST.get('resource_id') # Get the resource ID
            resource = get_object_or_404(EducationalResource, id=resource_id)  # Get the resource
            Comment.objects.create(resource=resource, user=request.user, text=text)
            messages.success(request, "Your comment has been posted!")
        elif 'question_title' in request.POST:  # Asking a question
            title = request.POST['question_title']
            description = request.POST['question_description']
            Question.objects.create(patient=request.user, title=title, description=description)
            messages.success(request, "Your question has been posted!")
        elif 'answer_text' in request.POST:  # Answering a question
            question_id = request.POST['question_id']
            question = get_object_or_404(Question, id=question_id)
            response = request.POST['answer_text']
            Answer.objects.create(question=question, doctor=request.user, response=response)
            messages.success(request, "Your answer has been posted!")

    return render(request, 'educational_resources.html', {'resources': resources})
def add_educational_resource (request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        file = request.FILES.get('file')
        video_url = request.POST.get('video_url')

        if title and description:
            EducationalResource.objects.create(
            title=title,
            description=description,
            category=category,
            file=file,
            video_url=video_url,
            uploaded_by=request.user,
        )

        return redirect('educational_resources_list')
    return render(request, 'add_educational_resource.html')
