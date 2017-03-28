require 'rake'
require 'rake/clean'

VENV_DIR = '.venv'.freeze

SORT_BY_ID = 'sort -unk 1,1'.freeze

ORIGINAL_DOCUMENT_FILE = 'travel02_userReview_20100713.txt'.freeze
ORIGINAL_LABEL_FILE = 'travel01_userEvaluation_20100713.txt'.freeze

DOCUMENT_FILE = 'documents.txt'.freeze
LABEL_FILE = 'labels.csv'.freeze
EXAMPLE_FILE = 'examples.txt'.freeze

DATASET_DIRS = %w(train develop test).freeze
VOCABULARY_FILES = %w(words.txt chars.txt).freeze

[ORIGINAL_LABEL_FILE, ORIGINAL_DOCUMENT_FILE].each do |f|
  file f do
    sh "nkf -Lu -w #{File.join '/coin/data/rakuten/old', f} > #{f}"
  end
end

file LABEL_FILE => ORIGINAL_LABEL_FILE do |t|
  sh "cut -f 1,7-13 #{t.source} | #{SORT_BY_ID} > #{t.name}"
end

file DOCUMENT_FILE => ORIGINAL_DOCUMENT_FILE do |t|
  sh %(cut -f 2,3 #{t.source} | \
        awk -F '	' '{print $2,$1}' OFS='	' | \
        #{SORT_BY_ID} | \
        sed -e 's/【ご利用の宿泊プラン】.*$//g' | \
        sed -e 's/[[:blank:]]*	[[:blank:]]*/	/g' -e 's/[[:blank:]]*$//g' | \
        sed -e '/^[^	]*	$/d' -e '/^	[^	]*$/d' -e '/^[^	]*$/d' > #{t.name})
end

file EXAMPLE_FILE => [LABEL_FILE, DOCUMENT_FILE] do |t|
  sh "join -t '	' #{t.sources.join ' '} | #{SORT_BY_ID} > #{t.name}"
end

def vsh(*args)
  sh ". #{VENV_DIR}/bin/activate && #{args.join ' '}"
end

task dataset: EXAMPLE_FILE do |t|
  unless Dir.exist? 'train'
    sh "rm -rf #{VENV_DIR}; python3 -m venv #{VENV_DIR}"
    vsh 'pip3 install --upgrade --no-cache-dir '\
        'nltokeniz gargparse mecab-python3'
    vsh 'python3 -m nltk.downloader punkt'
    vsh %W(python3 bin/rakuten2json.py
           --train_data_size 300000
           --develop_data_size 10000
           --test_data_size 10000
           #{t.source})
  end
end

DATASET_DIRS.each do |dir|
  directory dir => :dataset
end

task vocabularies: DATASET_DIRS[0..1] do |t|
  sh %W(python3 bin/create_vocabularies.py --min_freq #{ENV['min_freq'] || 0}
        #{t.sources.join ' '}).join(' ')
end

VOCABULARY_FILES.each do |filename|
  file filename => :vocabularies
end

task default: [*DATASET_DIRS, *VOCABULARY_FILES]

CLEAN.include Dir.glob(%w(*.txt *.csv))
CLOBBER.include %w(.venv train develop test)
