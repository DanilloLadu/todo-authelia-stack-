from flask import Flask, request, redirect, url_for, render_template_string
app = Flask(__name__)
def require_group(group):
    def decorator(f):
        def wrapper(*args, **kwargs):
            groups_header = request.headers.get("Remote-Groups", "")
            groups = [g.strip() for g in groups_header.split(",")]
            if group not in groups:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator
todos = []
HTML = """
<h1>Todo App</h1>
<form method="post">
<input name="task">
<button>Add</button>
</form>
<ul>
{% for todo in todos %}
<li>{{todo}}</li>
{% endfor %}
</ul>

<!-- Logout knop -->
<a href="{{ url_for('logout') }}">
    <button type="button">Logout</button>
</a>
"""
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            todos.append(task)
        return redirect(url_for("index"))
    return render_template_string(HTML, todos=todos)

@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            todos.append(task)
        return redirect(url_for("index"))
    return render_template_string(HTML, todos=todos)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/logout")
def logout():
    todos.clear() 
    # Redirect naar Authelia logout
    authelia_logout_url = "https://auth.todo.local/logout?rd=https://todo.local/"
    return redirect(authelia_logout_url)

@app.route("/me")
def me():
    user = request.headers.get("Remote-User")
    groups = request.headers.get("Remote-Groups")
    return {"user": user, "groups": groups}

@app.route("/admin")
@require_group("admins")
def admin():
    user = request.headers.get("Remote-User")
    groups = request.headers.get("Remote-Groups")
    return {"user": user, "groups": groups}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)