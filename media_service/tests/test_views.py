import unittest
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from media_service.models import MediaStore, Course, Collection, CourseImage, CollectionImage

class TestCourseEndpoint(APITestCase):
    fixtures = ['test.json']

    def get_example_item(self, detail=False):
        example_item = {
            "url": "http://localhost:8000/courses/1",
            "id": "1",
            "title": "Test",
            "collections_url": "http://localhost:8000/courses/1/collections",
            "images_url": "http://localhost:8000/courses/1/images",
            "lti_context_id": "asdf",
            "lti_tool_consumer_instance_guid": "asdf.canvas.localhost",
            "created": "2015-12-15T15:42:33.443434Z",
            "updated": "2015-12-15T15:42:33.443434Z",
            "type": "courses",
        }
        if detail:
            example_item.update({
                "images": [
                    {
                        "url": "http://localhost:8000/course-images/1",
                        "upload_url": "http://localhost:8000/course-images/1/upload",
                        "id": 1,
                        "course_id": 1,
                        "title": "Example Image",
                        "description": "",
                        "sort_order": 0,
                        "upload_file_name": None,
                        "created": "2015-12-15T15:42:33.443434Z",
                        "updated": "2015-12-15T15:42:33.443434Z",
                        "type": "courseimages",
                        "is_upload": False,
                        "thumb_height": None,
                        "thumb_width": None,
                        "image_type": None,
                        "image_width": None,
                        "image_height": None,
                        "image_url": None,
                        "thumb_url": None
                    },
                ],
                "collections": [
                    {
                        "url": "http://localhost:8000/collections/1",
                        "id": 1,
                        "title": "Example Collection",
                        "description": "",
                        "sort_order": 1,
                        "course_id": 1,
                        "course_image_ids": [1],
                        "images_url": "http://localhost:8000/collections/1/images",
                        "created": "2015-12-15T15:42:33.443434Z",
                        "updated": "2015-12-15T15:42:33.443434Z",
                        "type": "collections"
                    },
                ],
            })
        return example_item

    def test_course_list(self):
        courses = Course.objects.all()
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(courses))
        
        # Example of what we would expect
        example_item = self.get_example_item()
        expected_keys = sorted(example_item.keys())
        for course_data in response.data:
            actual_keys = sorted(course_data.keys())
            self.assertEqual(actual_keys, expected_keys)
    
    def test_course_detail(self):
        pk = 1
        course = Course.objects.get(pk=pk)
        url = reverse('course-detail', kwargs={"pk": pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get an example response item
        example_item = self.get_example_item(detail=True)
        expected_keys = sorted(example_item.keys())
        
        # Check course attributes
        nested_keys = ("images", "collections")
        course_keys = sorted([k for k in response.data if k not in nested_keys])
        expected_course_keys = sorted([k for k in example_item.keys() if k not in nested_keys])
        self.assertEqual(course_keys, expected_course_keys)
        self.assertTrue(all([ k in response.data for k in nested_keys ]))
        
        # Check nested items
        for nested_key in nested_keys:
            self.assertTrue(len(example_item[nested_key]) > 0)
            expected_image_keys = sorted([k for k in example_item[nested_key][0].keys()])
            for item in response.data[nested_key]:
                item_keys = sorted([k for k in item])
                self.assertEqual(item_keys, expected_image_keys)

    def test_create_course(self):
        url = reverse('course-list')
        body = {
            "title": "Test Course", 
            "lti_context_id": "e4d7f1b4ed2e42d15898f4b27b019da4",
            "lti_tool_consumer_instance_guid": "test.localhost"
        }

        # Create the new course
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the fields we submitted are reflected in a course object
        self.assertTrue('id' in response.data)
        self.assertTrue(Course.objects.filter(pk=response.data['id']).exists())
        created_course = Course.objects.get(pk=response.data['id'])
        for f in body:
            self.assertEqual(response.data[f], body[f])
            self.assertEqual(getattr(created_course, f), body[f])

    def test_delete_course(self):
        pk = 1
        url = reverse('course-detail', kwargs={"pk":pk})
        response = self.client.delete(url)
        self.assertTrue(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(pk=pk).exists())

    def test_update_course(self):
        pk = 1
        url = reverse('course-detail', kwargs={"pk": pk})
        body = {
            "title": "Title Updated(!)",
            "lti_context_id": "updated_context_id",
            "lti_tool_consumer_instance_guid": "updated_guid" 
        }

        # Show that our update differs from the existing course object
        course_before_update = Course.objects.get(pk=pk)
        for f in body:
            self.assertNotEqual(getattr(course_before_update, f), body[f])
        
        # Do the update
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Show that the updates were returned in the response and
        # are reflected in the course object
        course_after_update = Course.objects.get(pk=pk)
        for f in body:
            self.assertEqual(response.data[f], body[f])
            self.assertEqual(getattr(course_after_update, f), body[f])

    def test_add_collection_to_course(self):
        pk = 1
        url = reverse('course-collections', kwargs={"pk": pk})
        body = {
            "title": "Test Collection", 
            "description": "Some description",
        }

        # Create the new collection
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the fields we submitted are reflected in a course object
        self.assertTrue('id' in response.data)
        self.assertTrue(Collection.objects.filter(pk=response.data['id']).exists())
        created_collection = Collection.objects.get(pk=response.data['id'])
        self.assertEqual(created_collection.course.pk, pk)
        for f in body:
            self.assertEqual(response.data[f], body[f])
            self.assertEqual(getattr(created_collection, f), body[f])
    
class TestCollectionEndpoint(APITestCase):
    fixtures = ['test.json']

    def test_collection_list(self):
        collections = Collection.objects.all()
        url = reverse('collection-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(collections))
        
        # Example of what we would expect
        example_item = {
            "url": "http://localhost:8000/collections/1",
            "id": 1,
            "title": "Scrambled Eggs Super!",
            "description": "",
            "sort_order": 1,
            "course_id": 1,
            "course_image_ids": [1,4],
            "images_url": "http://localhost:8000/collections/1/images",
            "created": "2015-12-15T15:42:33.443434Z",
            "updated": "2016-01-06T21:13:08.353908Z",
            "type": "collections"
        }
        expected_keys = sorted(example_item.keys())
        for collection_data in response.data:
            actual_keys = sorted(collection_data.keys())
            self.assertEqual(actual_keys, expected_keys)

    def test_collection_detail(self):
        pk = 1
        course = Collection.objects.get(pk=pk)
        url = reverse('collection-detail', kwargs={"pk": pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get an example response item
        example_item = {
            "url": "http://localhost:8000/collections/1",
            "id": 1,
            "title": "Scrambled Eggs Super!",
            "description": "",
            "sort_order": 1,
            "course_id": 1,
            "course_image_ids": [1,4],
            "images": [],
            "images_url": "http://localhost:8000/collections/1/images",
            "created": "2015-12-15T15:42:33.443434Z",
            "updated": "2016-01-06T21:13:08.353908Z",
            "type": "collections"
        }
        expected_keys = sorted(example_item.keys())
        actual_keys = sorted(response.data.keys())
        self.assertEqual(actual_keys, expected_keys)

    def test_create_collection(self):
        url = reverse('collection-list')
        body = {
            "title": "Test Collection", 
            "description": "Some description",
            "course_id": 1,
        }

        # Create the new collection
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the fields we submitted are reflected in a course object
        self.assertTrue('id' in response.data)
        self.assertTrue(Collection.objects.filter(pk=response.data['id']).exists())
        created_collection = Collection.objects.get(pk=response.data['id'])
        for f in body:
            self.assertEqual(response.data[f], body[f])
            self.assertEqual(getattr(created_collection, f), body[f])

    def test_delete_collection(self):
        pk = 1
        url = reverse('collection-detail', kwargs={"pk":pk})
        response = self.client.delete(url)
        self.assertTrue(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Collection.objects.filter(pk=pk).exists())

    def test_update_collection(self):
        pk = 1
        url = reverse('collection-detail', kwargs={"pk": pk})
        collection = Collection.objects.get(pk=pk)
        body = {
            "title": "Thidwick The Big-Hearted Moose",
            "description": 'Thidwick the big-hearted moose is happy his antlers "can be of some use" to a menagerie of animals who move in and make themselves at home.',
            "course_id": collection.course.pk,
            "course_image_ids": [1,2,3,4],
        }

        # Do the update
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Show that the updates were returned in the response and
        # are reflected in the course object
        collection_after_update = Collection.objects.get(pk=pk)
        for f in ('title', 'description', 'course_id'):
            self.assertEqual(response.data[f], body[f])

        course_image_ids = collection_after_update.images.values_list('course_image__pk', flat=True)
        self.assertSequenceEqual(response.data['course_image_ids'], course_image_ids)
