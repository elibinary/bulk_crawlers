require 'net/http'
require 'nokogiri'
require 'open-uri'
require "base64"
require 'fileutils'

def fetch_urls
  @urls = File.readlines("url_list.txt")
  used_url = []

  @urls.each do |url|
    res = fetch_contents(url)
    unless res.is_a? Array
      if res
        used_url << url
      end
    end
  end

  begin
    f = File.new("用过的链接(除了参考它毫无价值).txt", "a+")
    used_url.each do |url|
      f.write(url)
      f.write("\n\n")
    end
  rescue Exception => e
  ensure
    f.close
  end
end

def fetch_contents(url)
  return false unless url_filter(url)
  uri = URI(url)
  req = Net::HTTP::Get.new(uri)
  req['Accept-Encoding'] = "none"
  begin
    res = Net::HTTP.start(uri.hostname, uri.port) {|http| http.request(req) }
    doc = Nokogiri::HTML(res.body)
    if doc
      parse_html(doc)
    end
  rescue Exception => e
  ensure
    return [false, url]
  end
end

def parse_html(doc)
  imgs = []
  con = doc.css('div#page-content div#img-content')
  title = con.css('h2#activity-name')[0].text.strip
  auth = con.css('a#post-user')[0].text.strip
  con_body = con.css('div#js_content')

  begin
    FileUtils::mkdir_p "#{Base64.urlsafe_encode64(title)}/img"
    f = File.new("#{Base64.urlsafe_encode64(title)}/#{title}.txt", "a+")

    f.write(title)
    f.write("\n\n")
    f.write(auth)
    f.write("\n\n\n")

    con_body.css('p').each do |p|
      if p.text.strip.length != 0
        f.write(p.text)
        f.write("\n\n")
      elsif p.css('img').any?
        img = p.css('img')[0].attributes["data-src"].value
        f.write(img)
        f.write("\n")
        f.write("(#{Base64.urlsafe_encode64(img)})")
        f.write("\n\n")
        imgs << img
      end
    end
  rescue Exception => e
    puts e
  ensure
    f.close
  end

  imgs.each do |img_url|
    load_img(img_url, title)
  end
end

def load_img(img, title)
  begin
    open("#{Base64.urlsafe_encode64(title)}/img/#{Base64.urlsafe_encode64(img)}.png", 'wb') do |file|
      file << open(img).read
    end
  rescue Exception => e
    puts e
  end
end

def url_filter(url)
  filter = 'mp.weixin.qq.com'
  url.match(filter) ? true : false
end
