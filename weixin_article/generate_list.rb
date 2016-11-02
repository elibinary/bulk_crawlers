# http://food.boohee.com/fb/v1/food_news?page=1

require 'net/http'
require 'json'

@uri = URI('http://food.boohee.com/fb/v1/food_news')


def request_urls(page)
  params = {
    page: page
  }
  @uri.query = URI.encode_www_form(params)
  res = Net::HTTP.get_response(@uri)

  if res.is_a?(Net::HTTPSuccess) && res.body 
    data = JSON.parse(res.body)
    return data["food_news"]
  end
  []
end

def build_file(obj_arr)
  begin
    f = File.new("url_list.txt", "a+")
    obj_arr.each do |obj|
      f.write(obj["link"])
      f.write("\n")
    end
  rescue Exception => e
    puts e
  ensure
    f.close
  end
end

def main
  i = 1
  res_arr = [1]
  while i < 100 && res_arr
    res_arr = request_urls(i)
    build_file(res_arr)
    i += 1
  end
end

main
# def url_filter(url)
  
# end
