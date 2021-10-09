from django.test import TestCase
from django.utils import timezone
import datetime, pytz
from .models import Event
from .search import make_search


# Create your tests here.

class EventModelTest(TestCase):
    def test_string_representation(self):
        event = Event(title = "My event title")
        self.assertEqual(str(event), event.title)

    def test_invalid_representation(self):
        event = Event(title = "My event title 2")
        self.assertNotEqual(str(event), "My event title 1")

    def test_valid_address(self):
        event = Event(title = "My event title")
        address = "291 McCormick Rd, Charlottesville, VA 22903"
        self.assertTrue(event.valid_address(address))

    def test_invalid_address(self):
        event = Event(title = "My event title")
        address = "44587 4245 Virginia, CO, New York"
        self.assertFalse(event.valid_address(address))

    def test_no_address(self):
        event = Event(title = "My event title")
        address = ""
        self.assertFalse(event.valid_address(address))

    def test_valid_time(self):
        event = Event(title = "My event title")
        time = timezone.now() + datetime.timedelta(days = 30)
        self.assertTrue(event.valid_time(time))

    def test_invalid_time(self):
        event = Event(title = "My event title")
        time = timezone.now() - datetime.timedelta(days = 30)
        self.assertFalse(event.valid_time(time))

    def test_null_time(self):
        event = Event(title = "My event title")
        time = None
        self.assertFalse(event.valid_time(time))

    def test_date_format(self):
        event = Event(title = "My event title")
        time = "2020-10-21T20:00"
        self.assertTrue(event.valid_date_format(time))

    def test_invalid_date_format(self):
        event = Event(title = "My event title")
        time = "November 20th, 2020"
        self.assertFalse(event.valid_date_format(time))

    def test_none_date_format(self):
        event = Event(title = "My event title")
        time = ""
        self.assertFalse(event.valid_date_format(time))
    
    def test_valid_interval(self):
        event = Event(title = "My event title")
        time1 = pytz.utc.localize(datetime.datetime.strptime("4000-10-21T20:00", '%Y-%m-%dT%H:%M'))
        time2 = pytz.utc.localize(datetime.datetime.strptime("4001-10-21T20:00", '%Y-%m-%dT%H:%M'))
        self.assertTrue(event.valid_interval(time1,time2))

    def test_invalid_interval(self):
        event = Event(title = "My event title")
        time1 = pytz.utc.localize(datetime.datetime.strptime("4001-10-21T20:00", '%Y-%m-%dT%H:%M'))
        time2 = pytz.utc.localize(datetime.datetime.strptime("4000-10-21T20:00", '%Y-%m-%dT%H:%M'))
        self.assertFalse(event.valid_interval(time1,time2))

    # exists_required_input tests
    def test_no_errors(self):
        event = Event(title = "My event title")
        name = event.title
        location = "The Rotunda"
        address = "830 Summit View Ln, Charlottesville, VA 22903"
        desc = "Lorem ipsum"
        start = pytz.utc.localize(datetime.datetime.strptime("4000-10-21T20:00", '%Y-%m-%dT%H:%M'))
        end = pytz.utc.localize(datetime.datetime.strptime("4001-10-21T20:00", '%Y-%m-%dT%H:%M'))
        self.assertEquals(event.exists_required_input(name, desc, location, address, start, end), 0)

    def test_error_1(self):
        event = Event(title = "")
        name = event.title
        location = "The Rotunda"
        address = "830 Summit View Ln, Charlottesville, VA 22903"
        desc = "Lorem ipsum"
        start = pytz.utc.localize(datetime.datetime.strptime("4000-10-21T20:00", '%Y-%m-%dT%H:%M'))
        end = pytz.utc.localize(datetime.datetime.strptime("4001-10-21T20:00", '%Y-%m-%dT%H:%M'))
        self.assertEquals(event.exists_required_input(name, desc, location, address, start, end), 1)

    def test_error_2(self):
        event = Event(title = "My event title")
        name = event.title
        location = ""
        address = "830 Summit View Ln, Charlottesville, VA 22903"
        desc = "Lorem ipsum"
        start = pytz.utc.localize(datetime.datetime.strptime("4000-10-21T20:00", '%Y-%m-%dT%H:%M'))
        end = pytz.utc.localize(datetime.datetime.strptime("4001-10-21T20:00", '%Y-%m-%dT%H:%M'))
        self.assertEquals(event.exists_required_input(name, desc, location, address, start, end), 2)

    def test_error_3(self):
        event = Event(title = "My event title")
        name = event.title
        location = "The Rotunda"
        address = "830 Summit View Ln, Charlottesville, VA 22903"
        desc = ""
        start = pytz.utc.localize(datetime.datetime.strptime("4000-10-21T20:00", '%Y-%m-%dT%H:%M'))
        end = pytz.utc.localize(datetime.datetime.strptime("4001-10-21T20:00", '%Y-%m-%dT%H:%M'))
        self.assertEquals(event.exists_required_input(name, desc, location, address, start, end), 3)

    def test_error_4(self):
        event = Event(title = "My event title")
        name = event.title
        location = "The Rotunda"
        address = "830 Summit View Ln, Charlottesville, VA 22903"
        desc = "Lorem ipsum"
        end = pytz.utc.localize(datetime.datetime.strptime("4000-10-21T20:00", '%Y-%m-%dT%H:%M'))
        start = pytz.utc.localize(datetime.datetime.strptime("4001-10-21T20:00", '%Y-%m-%dT%H:%M'))
        self.assertEquals(event.exists_required_input(name, desc, location, address, start, end), 4)

    def test_error_5(self):
        event = Event(title = "My event title")
        name = event.title
        location = "The Rotunda"
        address = "The Rotunda, Charlottesville, VA"
        desc = "Lorem ipsum"
        start = pytz.utc.localize(datetime.datetime.strptime("4000-10-21T20:00", '%Y-%m-%dT%H:%M'))
        end = pytz.utc.localize(datetime.datetime.strptime("4001-10-21T20:00", '%Y-%m-%dT%H:%M'))
        self.assertEquals(event.exists_required_input(name, desc, location, address, start, end), 0)

    def test_valid_event_json(self): 
        event = Event(title = "My event title", address = "4201 Stringfellow Rd, Chantilly, VA 20151")
        event_json = []
        event_json.append({"title": event.title, "address": event.address})
        self.assertEquals(event_json, [{"title": "My event title", "address": "4201 Stringfellow Rd, Chantilly, VA 20151"}])

    def test_invalid_event_json(self):
        event = Event(title = "My event title", address = "4201 Stringfellow Rd, Chantilly, VA 20151")
        event_json = []
        event_json.append({"title": event.title, "address": event.address})
        self.assertNotEqual(event_json, [{"title": "My event title", "address": "4202 Stringfellow Rd, Chantilly, VA 20151"}])

class SearchTests(TestCase):
    def test_exact_Title(self):
        event1 = Event(title="My event title")
        event2 = Event(title="Event2")
        event_list = [event1, event2]
        found_events = make_search("My event title", event_list)
        correct_list = [event1]
        self.assertEqual(correct_list, found_events)

    def test_partial_title(self):
        event1 = Event(title="My event title")
        event2 = Event(title="Event2")
        event_list = [event1, event2]
        found_events = make_search("title", event_list)
        correct_list = [event1]
        self.assertEqual(correct_list, found_events)

    def test_exact_location(self):
        event1 = Event(location_name= "Newcomb")
        event2 = Event(location_name="The Rotunda")
        event_list = [event1, event2]
        found_events = make_search("The Rotunda", event_list)
        correct_list = [event2]
        self.assertEqual(correct_list, found_events)

    def test_partial_location(self):
        event1 = Event(location_name= "Newcomb")
        event2 = Event(location_name="The Rotunda")
        event_list = [event1, event2]
        found_events = make_search("rotunda", event_list)
        correct_list = [event2]
        self.assertEqual(correct_list, found_events)

    def test_exact_description(self):
        event1 = Event(desc="A fun event!")
        event2 = Event(desc="A boring event")
        event_list = [event1, event2]
        found_events = make_search("A fun event!", event_list)
        correct_list = [event1]
        self.assertEqual(correct_list, found_events)

    def test_partial_description(self):
        event1 = Event(desc="A fun event!")
        event2 = Event(desc="A boring event")
        event_list = [event1, event2]
        found_events = make_search("fun event", event_list)
        correct_list = [event1]
        self.assertEqual(correct_list, found_events)

    def test_multiple_event_return(self):
        event1 = Event(title="My event title")
        event2 = Event(title="Event2: exam preparedness")
        event3 = Event(desc="a club meeting")
        event4 = Event(title="Exam prep meeting")
        event5 = Event(desc="exam prep for exam 5")
        event_list = [event1, event2, event3, event4, event5]
        found_events = make_search("exam prep", event_list)
        correct_list = [event2, event4, event5]
        self.assertEqual(correct_list, found_events)
