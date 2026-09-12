require 'jekyll'
require_relative '../_plugins/review_math'
converter = Jekyll::Converters::Markdown.new('markdown' => 'kramdown', 'kramdown' => {'input' => 'GFM'})
source = <<~'MD'
  $$
  c_t=\Phi_{\mathcal P}(\ell,o_t,h_t),\qquad a_t\in\mathcal A.
  $$

  $\mathbf{x}_t$ and $x_i < y_j$.

  ```bash
  echo "$value" "$other"
  ```
  `$literal$` and \$10.
MD
protected = ReviewMath.protect(source)
html = converter.convert(protected)
raise 'lost TeX' unless html.include?('c_t=\Phi_{\mathcal P}') && html.include?('$\mathbf{x}_t$')
raise 'math became emphasis' if html.include?('<em>')
raise 'unsafe less-than' unless html.include?('$x_i &lt; y_j$')
raise 'code was changed' unless protected.include?('echo "$value" "$other"') && protected.include?('`$literal$`')
raise 'currency was changed' unless protected.include?('\\$10')
raise 'not idempotent' unless ReviewMath.protect(protected) == protected
legacy = '<div markdown="0">' + "\n$$\nx_t\n$$\n</div>"
raise 'legacy broken' unless ReviewMath.protect(legacy) == legacy
raise 'escaped underscore changed' unless ReviewMath.protect('$\text{file\_name}$').include?('file\_name')
puts 'Review math: formulas, HTML safety, code, currency, legacy and idempotence PASS'

github = "```math\nx_t=\\left\\{y_t\\right\\}\n```\n$`x_i`$ and $`\\mathrm{Concat}`$\n"
rendered = converter.convert(ReviewMath.protect(github))
raise 'math fence lost TeX' unless rendered.include?('x_t=\\left\\{y_t\\right\\}')
raise 'quoted inline not math' unless rendered.include?('$x_i$') && rendered.include?('$\\mathrm{Concat}$')
raise 'math fence still code' if rendered.include?('<code')
puts 'GitHub math fences and quoted inline math PASS'
