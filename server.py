# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, Response, render_template, redirect, url_for, make_response, current_app, session, escape, helpers;

import config;

import json;

app = Flask(__name__);

@app.route('/')
def index():
  return render_template('index.html');

if __name__ == '__main__':
  app.run(host=config.attr('app_host'),port=config.attr('app_port'),debug=bool(config.attr('debug')));
