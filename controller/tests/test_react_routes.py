from app import app
from conftest import logged_in_client  # type: ignore
from flask import template_rendered
from tests.factories import UserFactory
from flask import template_rendered
from contextlib import contextmanager

@contextmanager
def captured_templates(app):
    # capture flask.render_template invocations
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class TestReactRoutes:
    def test_anonymous_user(self) -> None:
        with app.test_client() as client:
            with captured_templates(app) as templates:
                resp = client.get("/")
                assert resp.status_code == 200
                assert len(templates) == 1
                template, context = templates[0]
                assert template.name == "index.html"
                assert "preloaded_state" in context
                assert context["preloaded_state"]["user"] == {}

    def test_logged_in_user_preloaded_data(self) -> None:
        user = UserFactory.create()
        with logged_in_client(user) as client:
            with captured_templates(app) as templates:
                resp = client.get("/")
                assert resp.status_code == 200
                assert len(templates) == 1
                template, context = templates[0]
                assert template.name == "index.html"
                assert "preloaded_state" in context
                assert context["preloaded_state"]["user"] == {
                    "email": user.email,
                    "isActive": user.is_active,
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "userRole": user.user_role,
                }
