from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Conversation, Message
User = get_user_model()
 
 
@login_required
def inbox(request):
    """Show all conversations for the logged-in user."""
    conversations = Conversation.objects.filter(
        Q(student=request.user) | Q(tutor=request.user)
    ).select_related('student', 'tutor').prefetch_related('messages')
 
    # Annotate with unread count for the sidebar
    conv_data = []
    for conv in conversations:
        last_msg = conv.last_message()
        conv_data.append({
            'conversation': conv,
            'other_user': conv.get_other_user(request.user),
            'unread_count': conv.unread_count_for(request.user),
            'last_message': last_msg,
        })
 
    return render(request, 'messaging/inbox.html', {'conversations': conv_data})
 
 
@login_required
def conversation_detail(request, conversation_id):
    """Open a specific conversation and mark messages as read."""
    conversation = get_object_or_404(
        Conversation,
        Q(student=request.user) | Q(tutor=request.user),
        pk=conversation_id,
    )
    # Mark all unread messages from the other person as read
    conversation.messages.filter(is_read=False).exclude(
        sender=request.user
    ).update(is_read=True)
 
    messages = conversation.messages.select_related('sender').all()
    other_user = conversation.get_other_user(request.user)
 
    # All conversations for sidebar
    all_conversations = Conversation.objects.filter(
        Q(student=request.user) | Q(tutor=request.user)
    ).select_related('student', 'tutor').prefetch_related('messages')
 
    conv_data = []
    for conv in all_conversations:
        last_msg = conv.last_message()
        conv_data.append({
            'conversation': conv,
            'other_user': conv.get_other_user(request.user),
            'unread_count': conv.unread_count_for(request.user),
            'last_message': last_msg,
        })
 
    return render(request, 'messaging/conversation.html', {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user,
        'conversations': conv_data,
    })
 
 
@login_required
def start_conversation(request, tutor_id):
    """Start or resume a conversation with a tutor (called from tutor profile)."""
    tutor = get_object_or_404(User, pk=tutor_id)
    if tutor == request.user:
        return redirect('messaging:inbox')
 
    conversation, created = Conversation.objects.get_or_create(
        student=request.user,
        tutor=tutor,
    )
    return redirect('messaging:conversation', conversation_id=conversation.pk)
 
 
@login_required
@require_POST
def send_message(request, conversation_id):
    """Send a message in a conversation. Returns JSON for AJAX."""
    conversation = get_object_or_404(
        Conversation,
        Q(student=request.user) | Q(tutor=request.user),
        pk=conversation_id,
    )
    body = request.POST.get('body', '').strip()
    attachment = request.FILES.get('attachment')
 
    if not body and not attachment:
        return JsonResponse({'error': 'Message cannot be empty.'}, status=400)
 
    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        body=body,
        attachment=attachment,
    )
    # Bump conversation's updated_at so it surfaces at top of inbox
    conversation.save()
 
    return JsonResponse({
        'id': message.pk,
        'body': message.body,
        'sender_name': request.user.get_full_name() or request.user.username,
        'created_at': message.created_at.strftime('%I:%M %p'),
        'is_own': True,
        'attachment_url': message.attachment.url if message.attachment else None,
    })
 
 
@login_required
def unread_count(request):
    """API endpoint: total unread messages for the logged-in user (for navbar badge)."""
    count = Message.objects.filter(
        conversation__in=Conversation.objects.filter(
            Q(student=request.user) | Q(tutor=request.user)
        )
    ).filter(is_read=False).exclude(sender=request.user).count()
    return JsonResponse({'unread_count': count})

@login_required
def poll_messages(request, conversation_id):
    conversation = get_object_or_404(
        Conversation,
        Q(student=request.user) | Q(tutor=request.user),
        pk=conversation_id,
    )
    after_id = request.GET.get('after', 0)
    new_messages = conversation.messages.filter(
        pk__gt=after_id
    ).exclude(sender=request.user).select_related('sender')

    data = []
    for msg in new_messages:
        msg.mark_read()
        data.append({
            'id': msg.pk,
            'body': msg.body,
            'sender_name': msg.sender.get_full_name(),
            'created_at': msg.created_at.strftime('%I:%M %p'),
            'attachment_url': msg.attachment.url if msg.attachment else None,
        })

    return JsonResponse({'messages': data})
