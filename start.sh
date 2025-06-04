#!/usr/bin/env bash
gunicorn elc.wsgi:application --bind 0.0.0.0:$PORT
