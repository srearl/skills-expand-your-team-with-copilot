"""
Mock MongoDB database for development without MongoDB installation
"""

from argon2 import PasswordHasher
import copy

# In-memory storage
activities_data = {}
teachers_data = {}

# Methods
def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

class MockCollection:
    def __init__(self, data_dict):
        self.data = data_dict
    
    def count_documents(self, query):
        if not query:  # Empty query - count all
            return len(self.data)
        # For other queries, implement as needed
        return 0
    
    def insert_one(self, document):
        doc_id = document["_id"]
        doc_copy = copy.deepcopy(document)
        del doc_copy["_id"]
        self.data[doc_id] = doc_copy
        return None
    
    def find_one(self, query):
        if "_id" in query:
            doc_id = query["_id"]
            if doc_id in self.data:
                result = copy.deepcopy(self.data[doc_id])
                result["_id"] = doc_id
                return result
        return None
    
    def find(self, query=None):
        if query is None:
            query = {}
        
        results = []
        for doc_id, doc in self.data.items():
            doc_copy = copy.deepcopy(doc)
            doc_copy["_id"] = doc_id
            
            # Apply basic query filtering
            match = True
            for key, value in query.items():
                if key in doc_copy:
                    if isinstance(value, dict) and "$in" in value:
                        # Handle $in operator for arrays
                        if isinstance(doc_copy[key], list):
                            if not any(item in value["$in"] for item in doc_copy[key]):
                                match = False
                                break
                        else:
                            if doc_copy[key] not in value["$in"]:
                                match = False
                                break
                    elif isinstance(value, dict) and "$gte" in value:
                        # Handle $gte operator
                        if doc_copy[key] < value["$gte"]:
                            match = False
                            break
                    elif isinstance(value, dict) and "$lte" in value:
                        # Handle $lte operator
                        if doc_copy[key] > value["$lte"]:
                            match = False
                            break
                    elif isinstance(value, dict) and "$exists" in value:
                        # Handle $exists operator
                        field_exists = key in doc_copy
                        if field_exists != value["$exists"]:
                            match = False
                            break
                    elif doc_copy[key] != value:
                        match = False
                        break
                else:
                    # Handle case where field doesn't exist in document
                    if isinstance(value, dict) and "$exists" in value:
                        # $exists: False should match documents without the field
                        if value["$exists"]:
                            match = False
                            break
                    else:
                        match = False
                        break
            
            if match:
                results.append(doc_copy)
        
        return results
    
    def update_one(self, query, update):
        if "_id" in query:
            doc_id = query["_id"]
            if doc_id in self.data:
                if "$push" in update:
                    # Handle $push operation
                    for field, value in update["$push"].items():
                        if field not in self.data[doc_id]:
                            self.data[doc_id][field] = []
                        self.data[doc_id][field].append(value)
                        return type('MockResult', (), {'modified_count': 1})()
                elif "$pull" in update:
                    # Handle $pull operation
                    for field, value in update["$pull"].items():
                        if field in self.data[doc_id] and isinstance(self.data[doc_id][field], list):
                            if value in self.data[doc_id][field]:
                                self.data[doc_id][field].remove(value)
                                return type('MockResult', (), {'modified_count': 1})()
        return type('MockResult', (), {'modified_count': 0})()
    
    def aggregate(self, pipeline):
        # Simple implementation for getting unique days
        results = []
        for doc_id, doc in self.data.items():
            if "schedule_details" in doc and "days" in doc["schedule_details"]:
                for day in doc["schedule_details"]["days"]:
                    if {"_id": day} not in results:
                        results.append({"_id": day})
        
        # Sort alphabetically
        results.sort(key=lambda x: x["_id"])
        return results

# Create mock collections
activities_collection = MockCollection(activities_data)
teachers_collection = MockCollection(teachers_data)

def init_database():
    """Initialize database if empty"""
    
    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})
            
    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one({"_id": teacher["username"], **teacher})

# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "difficulty": "Beginner"
    },
    "Advanced Programming Workshop": {
        "description": "Advanced programming concepts and complex project development",
        "schedule": "Saturdays, 10:00 AM - 1:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "13:00"
        },
        "max_participants": 10,
        "participants": ["alex@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
        "difficulty": "Intermediate"
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
        "difficulty": "Beginner"
    },
    "Advanced Art Workshop": {
        "description": "Master advanced art techniques and portfolio development",
        "schedule": "Saturdays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 8,
        "participants": ["isabella@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        "difficulty": "Intermediate"
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"]
    },
    "Manga Maniacs": {
        "description": "Dive into epic adventures, forge unbreakable friendships, and discover worlds where anything is possible! Join fellow otaku as we explore the captivating universe of Japanese manga—from heart-pounding shonen battles to heartwarming slice-of-life stories. Share your favorite series, discover hidden gems, and unleash your inner artist as we celebrate the incredible art of storytelling that makes manga so irresistible!",
        "schedule": "Tuesdays, 7:00 PM - 8:30 PM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "19:00",
            "end_time": "20:30"
        },
        "max_participants": 15,
        "participants": []
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
     },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]