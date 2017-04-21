# tests.py
"""
here is the test file that will try the requests for us :)
"""
import unittest

from flask_testing import TestCase

from app import create_app, db

import os

from flask import abort, url_for

from app.models import Uye, Kategori, Kitap

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://lumenified88:tasocan88@localhost/kutuphane_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = Uye(email="admin@admin.com", username="admin", password="admin2016", is_admin=True)

        # create test non-admin user
        uye = Uye(username="test_user", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(uye)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestModels(TestBase):

    def test_uye_model(self):
        """
        Test number of records in our user table
        """
        self.assertEqual(Uye.query.count(), 2)

    def test_kategori_model(self):
        """
        Test number of records in Category table
        """

        # create test category
        kategori = Kategori(name="Hontoni")

        # save category to database
        db.session.add(kategori)
        db.session.commit()

        self.assertEqual(Kategori.query.count(), 1)

    def test_kitap_model(self):
        """
        Test number of records in __kitaplar__ (aka __books__) table
        """

        # create test a book
        kitap = Kitap(name="minna no nihongo aka herkesin japoncasi", description="introduction to the japanese ~101~")

        # save books to database
        db.session.add(kitap)
        db.session.commit()

        self.assertEqual(Kitap.query.count(), 1)

class TestViews(TestBase):
################################
########## Uye.views ########
#########################
    def test_anasayfa_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home.anasayfa'))
        self.assertEqual(response.status_code, 200)

    def test_giris_view(self):
        """
        Test that login page is accessible without login
        """
        response = self.client.get(url_for('uye.giris'))
        self.assertEqual(response.status_code, 200)

    def test_cikis_view(self):
        """
        Test that logout link is inaccessible without login
        and redirects to login page then to logout
        """
        target_url = url_for('uye.cikis')
        redirect_url = url_for('uye.giris', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

#####################################
############ home.views #############
#####################################

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('uye.giris', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('uye.giris', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
#####################################
####### admin.views###########
##########################
    def test_kategori_view(self):
        """
        Test that category page is inaccessible without login
        and redirects to login page then to category page
        """
        target_url = url_for('admin.kategori_liste')
        redirect_url = url_for('uye.giris', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_kitap_view(self):
        """
        Test that books page is inaccessible without login
        and redirects to login page then to books page
        """
        target_url = url_for('admin.kitap_liste')
        redirect_url = url_for('uye.giris', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_kiralama_view(self):
        """
        Test that renting page is inaccessible without login
        and redirects to login page then to renting page
        """
        target_url = url_for('admin.kiralama_listesi')
        redirect_url = url_for('uye.giris', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

if __name__ == '__main__':
    unittest.main()
