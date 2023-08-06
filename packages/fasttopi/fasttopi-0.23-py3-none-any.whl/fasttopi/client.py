import argparse
import requests

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title',help="the title to predict the categories for",type=str)
    args=parser.parse_args()
    return args

def validate_title(title):
    if not title:
        return False
    return len(title)> 7 and len(title)<= 100

def main():
    args = parse_args()
    title = args.title
    if not validate_title(title):
        print("please enter a title with the size of 7 to 100 characters")
    else:
        response = requests.get(f"http://127.0.0.1:80/categories/?title={title}")
        response = response.json()
        print(response["category"])



if __name__ == '__main__':
    main()