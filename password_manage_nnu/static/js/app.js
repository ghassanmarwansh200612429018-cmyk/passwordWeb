/* ========================================
   PassManNNU – JavaScript
   Theme toggle, Mobile menu, Toasts,
   Password tools (generate, copy, toggle)
   ======================================== */

document.addEventListener('DOMContentLoaded', () => {

    // ========== Dark Mode Toggle ==========
    const htmlEl = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    const themeToggleMobile = document.getElementById('theme-toggle-mobile');

    // Load saved preference
    if (localStorage.getItem('theme') === 'dark' ||
        (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        htmlEl.classList.add('dark');
    }

    function toggleTheme() {
        htmlEl.classList.toggle('dark');
        localStorage.setItem('theme', htmlEl.classList.contains('dark') ? 'dark' : 'light');
    }

    if (themeToggle) themeToggle.addEventListener('click', toggleTheme);
    if (themeToggleMobile) themeToggleMobile.addEventListener('click', toggleTheme);

    // ========== Mobile Menu ==========
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // ========== Message Toasts ==========
    const toasts = document.querySelectorAll('.message-toast');
    toasts.forEach((toast, i) => {
        setTimeout(() => {
            toast.classList.remove('translate-x-full', 'opacity-0');
            toast.classList.add('translate-x-0', 'opacity-100');
        }, i * 150);
        // Auto dismiss after 4s
        setTimeout(() => {
            toast.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => toast.remove(), 500);
        }, 4000 + i * 150);
    });

    // ========== Password Visibility Toggle ==========
    document.querySelectorAll('[data-toggle-password]').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-toggle-password');
            const input = document.getElementById(targetId);
            if (!input) return;

            if (input.type === 'password') {
                input.type = 'text';
                btn.innerHTML = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path></svg>`;
            } else {
                input.type = 'password';
                btn.innerHTML = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>`;
            }
        });
    });

    // ========== Copy to Clipboard ==========
    document.querySelectorAll('[data-copy]').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-copy');
            const input = document.getElementById(targetId);
            if (!input) return;

            const text = input.value || input.textContent;
            navigator.clipboard.writeText(text).then(() => {
                // Show "Copied!" feedback
                const original = btn.innerHTML;
                btn.innerHTML = `<span class="copied-feedback text-green-500 dark:text-green-400 text-xs font-semibold">Copied!</span>`;
                setTimeout(() => { btn.innerHTML = original; }, 1500);
            });
        });
    });

    // ========== Password Generator (client-side bridge to API) ==========
    document.querySelectorAll('[data-generate-password]').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-generate-password');
            const input = document.getElementById(targetId);
            const lengthInput = document.getElementById('password-length');
            const len = lengthInput ? lengthInput.value : 16;

            fetch(`/vault/generate-password/?length=${len}`)
                .then(r => r.json())
                .then(data => {
                    if (input) {
                        input.value = data.password;
                        input.type = 'text';  // show the generated password
                    }
                })
                .catch(err => console.error('Password generation failed:', err));
        });
    });

    // ========== Vault password display toggle ==========
    document.querySelectorAll('[data-reveal]').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-reveal');
            const el = document.getElementById(targetId);
            if (!el) return;
            if (el.getAttribute('data-hidden') === 'true') {
                el.textContent = el.getAttribute('data-value');
                el.setAttribute('data-hidden', 'false');
                btn.textContent = 'Hide';
            } else {
                el.textContent = '••••••••••••';
                el.setAttribute('data-hidden', 'true');
                btn.textContent = 'Show';
            }
        });
    });
});
