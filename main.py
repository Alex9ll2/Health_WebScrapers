from EmptyStringException import EmptyStringError
from scraperMiddleware import scraperMiddleware

def main():
    try:
        disease = input("Write your disease: ")
        scraperMiddleware(disease)
    except EmptyStringError:
        while not disease:
            disease = input("Write a disease: ")
            scraperMiddleware(disease)

if __name__ == "__main__":
    main()