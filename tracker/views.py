from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Task
from .forms import TaskForm

def task_list(request):
    """View to display all job/internship applications."""
    tasks = Task.objects.all()
    form = TaskForm()
    context = {
        'tasks': tasks,
        'form': form,
        'total_count': tasks.count(),
        'pending_count': tasks.filter(is_completed=False).count(),
        'completed_count': tasks.filter(is_completed=True).count(),
    }
    return render(request, 'tracker/task_list.html', context)

def add_task(request):
    """View to handle adding a new task/application."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tracker/add_task.html', {'form': form})

@require_POST
def complete_task(request, pk):
    """AJAX endpoint to mark a task as completed without page reload."""
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = True
    task.save()
    return JsonResponse({
        'success': True,
        'task_id': task.id,
        'status': 'Completed'
    })

@require_POST
def delete_task(request, pk):
    """Endpoint to delete a task from database and remove from UI."""
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return JsonResponse({'success': True, 'task_id': pk})
