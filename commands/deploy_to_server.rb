#!/usr/bin/env ruby -W0
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
require SUPPORT + "/environment.rb"
require CONTROLLERS_ROOT + "/deploy_controller.rb"
ENV["MM_CURRENT_PROJECT_DIRECTORY"] = ARGV[0]
dispatch :controller => "deploy", :action => "index"
