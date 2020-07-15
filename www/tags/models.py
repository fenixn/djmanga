import datetime
import os
import logging

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage

from django.db import models
from django.apps import apps

from django.utils import timezone
from django.utils.timezone import now

class Tag(models.Model):
    """
    A tag can be set to other models. Tags are useful for filtering
    """
    name = models.CharField(max_length=100) # The tag's name
    display = models.CharField(max_length=100, blank=True, null=True) # The tag's display name
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True) # A tag can be child to another Tag

    def __str__(self):
        if self.display:
            return self.display
        else:
            return self.name

    def get_by_name(name):
        """
        Returns the Tag object from a name input.
        Returns False if no match is found
        """
        tag_filter = Tag.objects.filter(
            name = name
        )
        if tag_filter.exists():
            return tag_filter.get()
        else:
            return False

    def get_book(self):
        """
        Returns all related Book
        """
        return self.book_set.all().order_by('name')

    def get_chapter(self):
        """
        Returns all related Chapter
        """
        return self.chapter_set.all().order_by('name')

    def get_tag_tree(self, tags):
        """
        Returns the tag tree structure
            tags: (models)  The input tags to organize into a tree structure
        """
        tag_tree = {} # The final tree to return
        tag_branches = {} # Holds tags that still needs organization
        for tag in tags:
            # Tags without a parent can go straight into the final tree
            if tag.parent is None: 
                tag_tree.update({tag: {}})
            else:
                tag_branches.update({tag: {}})
        # Calculate recursion level of each tag and sort from highest to lowest.
        # By attaching tag nodes in this order, we ensure all nodes gets linked.
        recursion_levels = {}
        for tag in tag_branches:
            tag_level = 1
            current_tag = tag
            while current_tag.parent in tag_branches:
                tag_level += 1
                current_tag = current_tag.parent
            recursion_levels[tag] = tag_level
        # Sort by recursion level
        recursion_levels = sorted(recursion_levels.items(), key=lambda x: x[1], reverse=True)
        sorted_unconnected_branches = {}
        for tag,level in recursion_levels:
            sorted_unconnected_branches.update({tag: {}})
        # Connect tag nodes in order to ensure they all get linked
        unconnected_branches = sorted_unconnected_branches.copy()
        for tag in unconnected_branches:
            if tag.parent in tag_branches:
                branch_tag = tag_branches[tag]
                tag_branches[tag.parent].update({tag:branch_tag})
                sorted_unconnected_branches.pop(tag)
        unconnected_branches = sorted_unconnected_branches.copy()
        for tag in unconnected_branches:
            branch_tag = tag_branches[tag]
            if tag.parent in tag_tree:
                tag_tree[tag.parent].update({tag:branch_tag})
                sorted_unconnected_branches.pop(tag)
        return tag_tree

    def get_all_tag_tree(self):
        """
        Returns the tree structure for all tags
        """
        tags = Tag.objects.all()
        return self.get_tag_tree(tags)