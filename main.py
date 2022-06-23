from models import Profile
from service import find_duplicates

if __name__ == "__main__":
    profile_one = {
        "first_name": "John",
        "last_name": "Doe",
        "class_year": 1,
        "date_of_birth": "2020-01-01",
        "email_field": "johndoe@gmail.com"
    }

    profile_two = {
        "first_name": "John",
        "last_name": "Doe",
        "class_year": 1,
        "date_of_birth": "2020-01-01",
        "email_field": "johndoe+asd@gmail.com"
    }

    fields = ["first_name", "last_name",
              "class_year", "date_of_birth", "email_field"]
    profile_one = Profile(**profile_one)
    profile_two = Profile(**profile_two)

    score, attributes = find_duplicates([profile_one, profile_two], fields)
    print("score", score)
    print("attributes", attributes)
