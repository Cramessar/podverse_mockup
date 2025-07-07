from app import create_app; from app.tasks.feed_task import auto_reparse_all; app = create_app(); with app.app_context(): result = auto_reparse_all(); print(result)
