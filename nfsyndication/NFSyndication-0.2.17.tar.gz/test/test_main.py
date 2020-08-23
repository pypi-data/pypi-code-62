from NFSyndication import config as NFSconfig
import os

os.mkdir('output')

subscriptions = [
  'http://feedpress.me/512pixels',
  'http://www.leancrew.com/all-this/feed/',
  'http://ihnatko.com/feed/',
  'http://blog.ashleynh.me/feed',
  'http://www.betalogue.com/feed/',
  'http://bitsplitting.org/feed/',
  'http://feedpress.me/jxpx777',
  'http://kieranhealy.org/blog/index.xml',
  'http://blueplaid.net/news?format=rss',
  'http://brett.trpstra.net/brettterpstra',
  'http://feeds.feedburner.com/NerdGap',
  'http://www.libertypages.com/clarktech/?feed=rss2',
  'http://feeds.feedburner.com/CommonplaceCartography',
  'http://kk.org/cooltools/feed',
  'http://danstan.com/blog/imHotep/files/page0.xml',
  'http://daringfireball.net/feeds/main',
  'http://david-smith.org/atom.xml',
  'http://feeds.feedburner.com/drbunsenblog',
  'http://stratechery.com/feed/',
  'http://www.gnuplotting.org/feed/',
  'http://feeds.feedburner.com/jblanton',
  'http://feeds.feedburner.com/IgnoreTheCode',
  'http://indiestack.com/feed/',
  'http://feedpress.me/inessential',
  'http://feeds.feedburner.com/JamesFallows',
  'http://feeds.feedburner.com/theendeavour',
  'http://feed.katiefloyd.me/',
  'http://feeds.feedburner.com/KevinDrum',
  'http://www.kungfugrippe.com/rss',
  'http://lancemannion.typepad.com/lance_mannion/rss.xml',
  'http://www.caseyliss.com/rss',
  'http://www.macdrifter.com/feeds/all.atom.xml',
  'http://mackenab.com/feed',
  'http://hints.macworld.com/backend/osxhints.rss',
  'http://macsparky.com/blog?format=rss',
  'http://www.macstories.net/feed/',
  'http://www.marco.org/rss',
  'http://merrillmarkoe.com/feed',
  'http://mjtsai.com/blog/feed/',
  'http://feeds.feedburner.com/mygeekdaddy',
  'http://nathangrigg.net/feed.rss',
  'http://onethingwell.org/rss',
  'http://schmeiser.typepad.com/penny_wiseacre/rss.xml',
  'http://feeds.feedburner.com/PracticallyEfficient',
  'http://robjwells.com/rss',
  'http://www.red-sweater.com/blog/feed/',
  'http://feedpress.me/sixcolors',
  'http://feedpress.me/candlerblog',
  'http://inversesquare.wordpress.com/feed/',
  'http://high90.com/feed',
  'http://joe-steel.com/feed',
  'http://feeds.veritrope.com/',
  'http://xkcd.com/atom.xml',
  'http://doingthatwrong.com/?format=rss']
  
with open(f'feeds.txt', 'w', encoding='utf8') as f:
    NFSconfig.init()
    f.write(",".join(subscriptions).replace(',', '\n'))
