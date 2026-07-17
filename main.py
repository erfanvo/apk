import flet as ft

def main(page: ft.Page):
    page.title = "Okala Smart App"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    # کادر دریافت جیسون
    json_input = ft.TextField(
        hint_text="📥 فایل JSON اکانت را اینجا پیست کنید...",
        multiline=True,
        min_lines=2,
        max_lines=3,
        text_align=ft.TextAlign.LEFT,
        dir="ltr",
        border_color=ft.colors.BLUE_400,
    )

    # مرورگر داخلی
    wv = ft.WebView(
        url="https://www.okala.com",
        expand=True,
        javascript_enabled=True
    )

    # تابع تزریق کدها به سایت
    def inject_click(e):
        if not json_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ اول متن JSON را وارد کن!", text_align=ft.TextAlign.CENTER))
            page.snack_bar.open = True
            page.update()
            return

        safe_json = json_input.value.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
        
        js_code = f"""
        try {{
            const accountData = JSON.parse(`{safe_json}`);
            localStorage.clear();
            sessionStorage.clear();
            document.cookie.split(";").forEach(c => {{ 
                document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
                document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/;domain=.okala.com"); 
            }});

            if (accountData.origins && accountData.origins[0] && accountData.origins[0].localStorage) {{
                accountData.origins[0].localStorage.forEach(item => {{
                    localStorage.setItem(item.name, item.value);
                }});
            }}

            if (accountData.cookies) {{
                const expireDate = new Date();
                expireDate.setFullYear(expireDate.getFullYear() + 1);
                accountData.cookies.forEach(cookie => {{
                    if(!cookie || !cookie.name || !cookie.value) return;
                    if(cookie.name.startsWith('TS01') || cookie.name.startsWith('_ga') || cookie.name.startsWith('_gcl')) return; 
                    document.cookie = `${{cookie.name}}=${{cookie.value}}; path=/; domain=.okala.com; expires=${{expireDate.toUTCString()}}`;
                }});
            }}
            window.location.reload();
        }} catch(err) {{
            alert("❌ فایل JSON معتبر نیست!");
        }}
        """
        wv.evaluate_javascript(js_code)

    # دکمه ورود
    btn = ft.ElevatedButton(
        "🚀 تزریق و ورود به اکانت", 
        on_click=inject_click, 
        width=float('inf'), 
        color=ft.colors.WHITE, 
        bgcolor=ft.colors.GREEN_700
    )

    # هدر بالای اپلیکیشن
    header = ft.Container(
        content=ft.Column([json_input, btn], spacing=5),
        padding=10,
        bgcolor=ft.colors.GREY_900
    )

    # اضافه کردن به صفحه
    page.add(ft.Column([header, wv], spacing=0, expand=True))

ft.app(target=main)
