from models import Author, Quote

import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def name(arg):
    arg = arg.strip()
    auth = Author.objects(fullname__istartswith=arg).first()
    if auth:
        quotes = Quote.objects(author=auth.id)
        print(f"Quotes of {auth.fullname}:")
        i = 1
        for quote in quotes:
            print(f"{i}. {quote.quote}")
            i += 1
    else:
        print(f"No author found with the name: {arg}")


@cache
def tag(args):
    quotes_list = []
    tag = args.strip().lower()
    quotes = Quote.objects()
    for quote in quotes:
        for i in range(len(quote.tags)):
            if (tag in quote.tags[i]) and (quote not in quotes_list):
                quotes_list.append(quote)
    if quotes_list:
        print(f"Quotes with tag \"{tag}\":")
        i = 1
        for quote in quotes_list:
            print(f"{i}. {quote.quote}")
            i += 1
    else:
        print(f"No tag \"{tag}\" found")


@cache
def tags(args):
    tags_list = args.split(",")
    tags_list = [tag.strip() for tag in tags_list]
    formatted_list = [f'"{item}"' for item in tags_list]
    result_string = ', '.join(formatted_list)
    quotes = Quote.objects(tags__in=tags_list)
    if quotes:
        print(f"Quotes with tags {result_string}:")
        i = 1
        for quote in quotes:
            print(f"{i}. {quote.quote}")
            i += 1
    else:
        print(f"No tags found: {result_string}")


if __name__ == '__main__':
    end = False
    while not end:
        text = input("Input command: ")
        if text.lower() == "exit":
            end = True
        else:
            try:
                command, args = text.split(":")
                command = command.replace(" ", "").lower()
                match command:
                    case 'name':
                        name(args)
                    case 'tag':
                        tag(args)
                    case 'tags':
                        tags(args)
                    case _:
                        print("Such command does not exist")
            except ValueError:
                print("Input command and arguments")