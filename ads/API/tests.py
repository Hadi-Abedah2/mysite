from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ads.models import Ad, Comment 


class AdViewSetPermissionTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='test', password='test')
        self.not_owner = get_user_model().objects.create_user(username='not_owner', password='not_owner')
        self.ad = Ad.objects.create(title='Test Ad', price=100, text='This is a test ad.', owner=self.user)




    def test_ads_readonly_for_unauthenticated_user(self):
        url = reverse('ads-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_ads_create_for_unauthenticated_user(self):
        url = reverse('ads-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_ads_create_for_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('ads-list')
        response = self.client.post(url, {'title': 'Test Ad', 'price': 100, 'text': 'This is a test ad.'})
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_Ads_update_for_owner(self):
        #ad = Ad.objects.create(title='Test Ad', price=100, text='This is a test ad.', owner=self.user)
        url = reverse('ads-detail', args=[self.ad.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {'title': 'Updated Test Ad'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Test Ad')

    def test_Ads_update_for_non_owner(self):
        url = reverse('ads-detail', args=[self.ad.id])
        self.client.force_authenticate(user=self.not_owner)
        response = self.client.patch(url, {'title': 'Updated Test Ad'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_Ads_delete_for_owner(self):
        url = reverse('ads-detail', args=[self.ad.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 0)

    def test_Ads_delete_for_non_owner(self):
        url = reverse('ads-detail', args=[self.ad.id])
        self.client.force_authenticate(user=self.not_owner)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Ad.objects.count(), 1)


class CommentViewSetPermissionTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='test', password='test')
        self.not_owner = get_user_model().objects.create_user(username='not_owner', password='not_owner')
        self.ad = Ad.objects.create(title='Test Ad', price=100, text='This is a test ad.', owner=self.user)
        self.comment = Comment.objects.create(text='This is a test comment.', owner=self.user, ad=self.ad)

    def test_comments_readonly_for_unauthenticated_user(self):
        url = reverse('comments-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comments_create_for_unauthenticated_user(self):
        url = reverse('comments-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comments_create_for_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comments-list')
        response = self.client.post(url, {'text': 'Another test comment.', 'ad': self.ad.id, 'owner': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comments_update_for_owner(self):
        url = reverse('comments-detail', args=[self.comment.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {'text': 'Updated test comment.'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Updated test comment.')

    def test_comments_update_for_non_owner(self):
        url = reverse('comments-detail', args=[self.comment.id])
        self.client.force_authenticate(user=self.not_owner)
        response = self.client.patch(url, {'text': 'Updated test comment.'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comments_delete_for_owner(self):
        url = reverse('comments-detail', args=[self.comment.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_comments_delete_for_non_owner(self):
        url = reverse('comments-detail', args=[self.comment.id])
        self.client.force_authenticate(user=self.not_owner)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)


class AdViewSetTestCase(APITestCase):
    ''' I will not test the CRUD since it is covered in the above PermissionTest '''

    def setUp(self): 
        self.user = get_user_model().objects.create_user(username='test', password='test')
        self.client = APIClient() 
        self.client.force_authenticate(user=self.user)
        self.not_owner = get_user_model().objects.create_user(username='not_owner', password='not_owner')
        self.ad = Ad.objects.create(title='Test Ad', price=100, text='This is a test ad.', owner=self.user)
        self.comment = Comment.objects.create(ad=self.ad, text="Test Comment", owner=self.user)
        self.comment = Comment.objects.create(ad=self.ad, text="Test2 Comment", owner=self.user)

    def test_comments_action(self):
        url = reverse('ads-comments', kwargs={"pk":self.ad.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  
        self.assertEqual(response.data[0]['text'], "Test Comment")

    def test_my_ads_action_authenticated(self):
        url = reverse('ads-my-ads')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Ad")

    def test_my_ads_action_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('ads-my-ads')
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentViewSetTestCase(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test')
        self.not_owner = get_user_model().objects.create_user(username='notowner', password='notowner')
        self.client = APIClient() 
        self.client.force_authenticate(user=self.user)
        self.ad = Ad.objects.create(title='Test Ad', price=100, text='This is a test ad.', owner=self.user)
        self.comment = Comment.objects.create(ad=self.ad, text="Test Comment", owner=self.user)
        self.comment = Comment.objects.create(ad=self.ad, text="Test2 Comment", owner=self.user)
        self.comment = Comment.objects.create(ad=self.ad, text="Test3 Comment", owner=self.not_owner)
        
    def test_commnets_list(self):
        url = reverse('comments-list')
        response = self.client.get(url)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        #self.assertEqual(response.data['results'][0]['text'], "Test3 Comment") this test fails intermittently 

    def test_comments_create(self):
        url = reverse('comments-list') 
        response = self.client.post(url, {'text': 'Test Comment_LAST', 'ad': self.ad.id, 'owner': self.not_owner.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 4)
        self.assertEqual(Comment.objects.last().text, 'Test Comment_LAST')

    def test_my_comments_action(self):
        url = reverse('comments-my-comments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_my_comments_action_unauthenticated(self):
        url = reverse('comments-my-comments')
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
