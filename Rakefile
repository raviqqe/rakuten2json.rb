require 'rake'
require 'rake/clean'


VENV_DIR = '.venv'

SORT_BY_ID = 'sort -unk 1,1'

ORIGINAL_DOCUMENT_FILE = 'travel02_userReview_20100713.txt'
ORIGINAL_LABEL_FILE = 'travel01_userEvaluation_20100713.txt'

DOCUMENT_FILE = 'documents.txt'
LABEL_FILE = 'labels.csv'
EXAMPLE_FILE = 'examples.txt'



[ORIGINAL_LABEL_FILE, ORIGINAL_DOCUMENT_FILE].each do |f|
  file f do
    sh "nkf -Lu -w #{File.join '/coin/data/rakuten/old', f} > #{f}"
  end
end


file LABEL_FILE => ORIGINAL_LABEL_FILE do |t|
  sh "cut -f 1,7-13 #{t.source} | #{SORT_BY_ID} > #{t.name}"
end


file DOCUMENT_FILE => ORIGINAL_DOCUMENT_FILE do |t|
  sh %Q(cut -f 2,3 #{t.source} | \
        awk -F '	' '{print $2,$1}' OFS='	' | \
        #{SORT_BY_ID} | \
        sed -e 's/【ご利用の宿泊プラン】.*$//g' | \
        sed -e 's/[[:blank:]]*	[[:blank:]]*/	/g' -e 's/[[:blank:]]*$//g' | \
        sed -e '/^[^	]*	$/d' -e '/^	[^	]*$/d' -e '/^[^	]*$/d' > #{t.name})
end


file EXAMPLE_FILE => [LABEL_FILE, DOCUMENT_FILE] do |t|
  sh "join -t '	' #{t.sources.join ' '} | #{SORT_BY_ID} > #{t.name}"
end


def vsh *args
  sh ". #{VENV_DIR}/bin/activate && #{args.join ' '}"
end


task :default => EXAMPLE_FILE do |t|
  sh "rm -rf #{VENV_DIR}; python3 -m venv #{VENV_DIR}"
  vsh 'pip3 install --upgrade --no-cache-dir nltokeniz gargparse mecab-python3'
  vsh 'python3 -m nltk.downloader punkt'
  vsh %W(python3 bin/rakuten2json.py
      --train_data_size 300000
      --develop_data_size 10000
      --test_data_size 10000
      #{t.source})
end


CLEAN.include Dir.glob(%w(*.txt *.csv))
CLOBBER.include %w(.venv train develop test)
