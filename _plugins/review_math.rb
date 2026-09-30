# Keep review Markdown portable; HTML protection exists only during Jekyll rendering.
require 'cgi'

module ReviewMath
  TOKENS = /(?<legacy><div[ ]markdown="0">.*?<\/div>|<span[ ]markdown="0">.*?<\/span>)|(?<mathfence>^```math[ \t]*\n(?<mathbody>.*?)^```[ \t]*$)|(?<quoted>\$`(?<quotedbody>[^`\n]+)`\$)|(?<fence>^[ \t]*(?<ticks>`{3,}|~{3,})[^\n]*\n.*?^[ \t]*\k<ticks>[ \t]*$)|(?<code>(?<tick>`+)[^\n]*?\k<tick>)|(?<escaped>\\.)|(?<display>\$\$.*?\$\$)|(?<inline>\$(?![\s$])(?:\\.|[^$\n\\])*?(?<!\s)\$)/mx

  # Bare $...$/$$...$$ is ambiguous with currency and shell text, so only
  # reviews opt into it; GitHub math fences and $`...`$ are safe everywhere.
  def self.protect(content, legacy: true)
    content.gsub(TOKENS) do |token|
      match = Regexp.last_match
      if match[:mathfence]
        "\n<div markdown=\"0\">\n$$\n#{CGI.escapeHTML(match[:mathbody])}$$\n</div>\n"
      elsif match[:quoted]
        "<span markdown=\"0\">$#{CGI.escapeHTML(match[:quotedbody])}$</span>"
      elsif !legacy
        token
      elsif match[:display]
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
  review = %w[paper repo].include?(document.data['source_type'])
  document.content = ReviewMath.protect(document.content, legacy: review)
end
