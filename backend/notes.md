What I need to do


- Marshmallow'lar tamamlandiktan sonra onlari ekle dictionaries yerine routelerin icine
- try except blocks - bak bakalim after global error middleware nerede ihtiyacin olacak, hepsi gitmiyor ama azalabilir. genelde ikisini combine etmek daha mantikli ama dikkat et terminalde error gormeni engellemesinler 
- use error middleware for common errors for consistent format accross the wholw app
- Use try-except for specific Ccses->  Use try-except blocks in functions where you need specific error handling logic, resource management, or additional logging

/feeds/{id}/reparse
→ Controller triggers Celery task
→ Celery calls Feedparser logic (from service)

COMMANDS
cd .. && docker-compose exec backend python -m pytest tests/test_feeds.py -v
