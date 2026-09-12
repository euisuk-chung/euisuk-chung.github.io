# Keep review Markdown portable; HTML protection exists only during Jekyll rendering.
require 'cgi'

module ReviewMath
  TOKENS = /(?<legacy><div[ ]markdown="0">.*?<\/div>|<span[ ]markdown="0">.*?<\/span>)|(?<fence>^[ \t]*(?<ticks>`{3,}|~{3,})[^\n]*\n.*?^[ \t]*\k<ticks>[ \t]*$)|(?<code>(?<tick>`+)[^\n]*?\k<tick>)|(?<escaped>\\.)|(?<display>\$\$.*?\$\$)|(?<inline>\$(?![\s$])(?:\\.|[^$\n\\])*?(?<!\s)\$)/mx

  def self.protect(content)
    content.gsub(TOKENS) do |token|
      match = Regexp.last_match
      if match[:display]
        "\n<div markdown=\"0\">\n#{CGI.escapeHTML(token)}\n</div>\n"
      elsif match[:inline]
        "<span markdown=\"0\">#{CGI.escapeHTML(token)}</span>"
      else
        token
      end
    end
  end
end

Jekyll::Hooks.register :documents, :pre_render do |document|
  next unless %w[paper repo].include?(document.data['source_type'])
  document.content = ReviewMath.protect(document.content)
end
