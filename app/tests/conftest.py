""" pytest configuration: make the pure helper modules importable """
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../plot_app'))
