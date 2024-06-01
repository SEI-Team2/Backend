import os
from dotenv import load_dotenv
import multiprocessing

bind = "0.0.0.0:8080"
workers = 4