
from News.news import News

with News() as bot:
    bot.land_first_page()
    bot.getNews()
