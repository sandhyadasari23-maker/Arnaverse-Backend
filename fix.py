import re

with open('C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/main.js', 'r', encoding='utf-8') as f:
    code = f.read()

new_router = """    const isAdminRoute = path.startsWith('/admin-') && path !== '/admin-login';

    try {
        const routeLoader = routes[path] || routes['/'];
        const viewModule = await routeLoader();
        
        app.innerHTML = '';
        if (isAdminRoute) {
            app.innerHTML = `
                <div class="admin-layout">
                    ${renderAdminSidebar()}
                    <div class="admin-main">
                        <div id="view-container"></div>
                    </div>
                </div>
            `;
        } else if (path === '/admin-login' || path === '/login' || path === '/register') {
            app.innerHTML = `
                ${renderNavbar()}
                <div id="view-container"></div>
            `;
        } else {
            app.innerHTML = `
                ${renderNavbar()}
                <div id="view-container"></div>
                ${renderFooter()}
            `;
        }
        
        const viewContainer = document.getElementById('view-container');
        viewContainer.innerHTML = viewModule.render();
        if (viewModule.init) viewModule.init(params);
    } catch (err) {
        console.error("Routing error:", err);
        const app_el = document.getElementById('app');
        if (app_el) app_el.innerHTML = `<div style="padding: 100px; text-align: center;"><h2>404 - Page Not Found</h2></div>`;
    }
};"""

code = re.sub(r'    const isAdminRoute = path\.startsWith.*?^};', new_router, code, flags=re.DOTALL | re.MULTILINE)

with open('C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/main.js', 'w', encoding='utf-8') as f:
    f.write(code)
