#!/usr/bin/ruby
#usage: ruby sign_update.rb path_to_your_update.zip path_to_your_dsa_priv.pem
if ARGV.length < 2
  puts "Usage: ruby sign_update.rb update_archive private_key"
  exit
end

puts `openssl dgst -sha1 -binary < "#{ARGV[0]}" | openssl dgst -dss1 -sign "#{ARGV[1]}" | openssl enc -base64`