from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import JsonResponse

from .models import VaultEntry
from .encryption import encrypt_password, decrypt_password
from .utils import generate_password
from accounts.forms import PasskeyVerifyForm


@login_required
def vault_dashboard(request):
    """Display all vault entries for the logged-in user."""
    entries = VaultEntry.objects.filter(user=request.user)
    decrypted_entries = []
    for entry in entries:
        try:
            decrypted_pw = decrypt_password(entry.encrypted_password)
        except Exception:
            decrypted_pw = '*** decryption error ***'
        decrypted_entries.append({
            'id': entry.id,
            'website_name': entry.website_name,
            'username': entry.username,
            'email': entry.email,
            'password': decrypted_pw,
            'created_at': entry.created_at,
            'updated_at': entry.updated_at,
        })
    return render(request, 'vault/dashboard.html', {'entries': decrypted_entries})


@login_required
def add_entry(request):
    """Add a new vault entry."""
    if request.method == 'POST':
        website_name = request.POST.get('website_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not all([website_name, username, email, password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'vault/add_entry.html')

        VaultEntry.objects.create(
            user=request.user,
            website_name=website_name,
            username=username,
            email=email,
            encrypted_password=encrypt_password(password),
        )
        messages.success(request, 'Entry added successfully!')
        return redirect('vault_dashboard')

    generated_pw = generate_password()
    return render(request, 'vault/add_entry.html', {'generated_password': generated_pw})


@login_required
def edit_entry(request, entry_id):
    """Edit an existing vault entry. Requires passkey verification first."""
    entry = get_object_or_404(VaultEntry, id=entry_id, user=request.user)

    # Check if passkey has been verified for this entry in this session
    verified_key = f'passkey_verified_{entry_id}'
    if not request.session.get(verified_key):
        return redirect('verify_passkey', entry_id=entry_id, action='edit')

    if request.method == 'POST':
        website_name = request.POST.get('website_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not all([website_name, username, email, password]):
            messages.error(request, 'All fields are required.')
        else:
            entry.website_name = website_name
            entry.username = username
            entry.email = email
            entry.encrypted_password = encrypt_password(password)
            entry.save()
            # Clear verification flag
            request.session.pop(verified_key, None)
            messages.success(request, 'Entry updated successfully!')
            return redirect('vault_dashboard')

    try:
        decrypted_pw = decrypt_password(entry.encrypted_password)
    except Exception:
        decrypted_pw = ''

    generated_pw = generate_password()
    return render(request, 'vault/edit_entry.html', {
        'entry': entry,
        'decrypted_password': decrypted_pw,
        'generated_password': generated_pw,
    })


@login_required
def delete_entry(request, entry_id):
    """Delete a vault entry. Requires passkey verification first."""
    entry = get_object_or_404(VaultEntry, id=entry_id, user=request.user)

    verified_key = f'passkey_verified_delete_{entry_id}'
    if not request.session.get(verified_key):
        return redirect('verify_passkey', entry_id=entry_id, action='delete')

    if request.method == 'POST':
        entry.delete()
        request.session.pop(verified_key, None)
        messages.success(request, 'Entry deleted successfully!')
        return redirect('vault_dashboard')

    return render(request, 'vault/delete_entry.html', {'entry': entry})


@login_required
def verify_passkey(request, entry_id, action):
    """Verify user's passkey before edit/delete operations."""
    entry = get_object_or_404(VaultEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = PasskeyVerifyForm(request.POST)
        if form.is_valid():
            passkey = form.cleaned_data['passkey']
            profile = request.user.profile
            if check_password(passkey, profile.passkey_hash):
                # Mark as verified in session
                if action == 'edit':
                    request.session[f'passkey_verified_{entry_id}'] = True
                    return redirect('edit_entry', entry_id=entry_id)
                elif action == 'delete':
                    request.session[f'passkey_verified_delete_{entry_id}'] = True
                    return redirect('delete_entry', entry_id=entry_id)
            else:
                messages.error(request, 'Invalid passkey. Please try again.')
    else:
        form = PasskeyVerifyForm()

    return render(request, 'vault/verify_passkey.html', {
        'form': form,
        'entry': entry,
        'action': action,
    })


@login_required
def generate_password_api(request):
    """API endpoint to generate a random password (AJAX)."""
    length = int(request.GET.get('length', 16))
    password = generate_password(length)
    return JsonResponse({'password': password})
