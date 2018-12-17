import discord
import random
from discord.ext import commands
from utils.dataIO import fileIO
from utils.cog import Cog
from utils.embed import Embeds
from utils import checks
import os
import asyncio
import time
from datetime import datetime

class Fun(Cog):
    def __init__(self, *args, **kwargs):
        #
        self.lick = ['https://media.giphy.com/media/12MEJ2ArZc23cY/giphy.gif', 'https://media.giphy.com/media/x4P8TaYhGn4FW/giphy.gif', 'https://media.giphy.com/media/JUrjTvzTbTUME/giphy.gif', 
		'http://img0.joyreactor.com/pics/post/anime-gif-anime-lick-ice-cream-1107069.gif', 'http://media.giphy.com/media/8GiREm7aqMwN2/giphy.gif', 'https://media.tenor.co/images/1925e468ff1ac9efc2100a3d092c54ff/raw', 
		'http://78.media.tumblr.com/tumblr_mdilccZR9u1r41eqro1_500.gif', 'https://media.tenor.co/images/201069307ee18e161ddad73a87f1775c/tenor.gif', 'https://media.giphy.com/media/bq7b2v3pYp4MU/giphy.gif', 
		'http://images.rapgenius.com/abbb4fb420fb5becf35dc05ab9cdbe72.500x375x13.gif', 'https://media.giphy.com/media/VcB3UYMwOhHA4/giphy.gif', 'https://media.giphy.com/media/11dPyMQxP2xFqo/giphy.gif', 
		'https://media.giphy.com/media/NGALQBUgvmVTa/giphy.gif', 'https://media.giphy.com/media/DNkYWBa2GfCPC/giphy.gif', 'https://media.giphy.com/media/njFCFpI7tttoQ/giphy.gif', 
		'https://media.giphy.com/media/mUJlJj6u7y9Ow/giphy.gif', 'http://orig10.deviantart.net/20c8/f/2013/215/8/d/lick_2_by_anime_wolfz-d6gi186.gif', 'http://cdn1.smosh.com/sites/default/files/bloguploads/pokemon-gif-lick.gif', 
		'https://media.giphy.com/media/89AAoZicNaRsA/giphy.gif']

        #
        self.hug = ['http://25.media.tumblr.com/tumblr_m8223lqZCl1ra8wu5o1_500.gif','http://www.thehomeplanet.org/wp-content/uploads/2013/04/Bobby-Sam-Hug.gif','http://24.media.tumblr.com/tumblr_lw7r7vRUGN1qii6tmo1_500.gif', 
		'https://33.media.tumblr.com/680b69563aceba3df48b4483d007bce3/tumblr_mxre7hEX4h1sc1kfto1_500.gif', 'http://media.giphy.com/media/lrr9rHuoJOE0w/giphy.gif', 
		'https://38.media.tumblr.com/b004f301143edad269aa1d88d0f1e245/tumblr_mx084htXKO1qbvovho1_500.gif', 'http://img4.wikia.nocookie.net/__cb20130302231719/adventuretimewithfinnandjake/images/1/15/Tumblr_m066xoISk41r6owqs.gif', 
		'http://cdn.smosh.com/sites/default/files/ftpuploads/bloguploads/0413/epic-hugs-friends-anime.gif', 'http://1.bp.blogspot.com/-OpJBN3VvNVw/T7lmAw0HxFI/AAAAAAAAAfo/bGJks9CqbK8/s1600/HUG_K-On!+-+Kawaii.AMO.gif', 
		'http://media.tumblr.com/tumblr_m1oqhy8vrH1qfwmvy.gif', 'https://myanimelist.cdn-dena.com/s/common/uploaded_files/1461073447-335af6bf0909c799149e1596b7170475.gif',
		'http://24.media.tumblr.com/49a21e182fcdfb3e96cc9d9421f8ee3f/tumblr_mr2oxyLdFZ1s7ewj9o1_500.gif', 'http://pa1.narvii.com/5774/3cb894f1d4bcb4a9c58a06ee2a7fcd1a11f9b0eb_hq.gif',
		'http://media.tumblr.com/01949fb828854480b513a87fa4e8eee7/tumblr_inline_n5r8vyJZa61qc7mf8.gif','https://media.tenor.co/images/e07a54a316ea6581329a7ccba23aea2f/tenor.gif', 
		'http://media.giphy.com/media/aD1fI3UUWC4/giphy.gif', 'https://38.media.tumblr.com/3b6ccf23ecd9aeacfcce0add1462c7c0/tumblr_msxqo58vDq1se3f24o1_500.gif', 
		'https://myanimelist.cdn-dena.com/s/common/uploaded_files/1460992224-9f1cd0ad22217aecf4507f9068e23ebb.gif', 
		'http://25.media.tumblr.com/tumblr_m0lgriUiVK1rqfhi2o1_500.gif', 'http://media.tumblr.com/tumblr_lknzmbIG1x1qb5zie.gif', 'http://mrwgifs.com/wp-content/uploads/2013/04/Snuggling-Cuddling-Anime-Girls-Gif-.gif', 
		'https://38.media.tumblr.com/b004f301143edad269aa1d88d0f1e245/tumblr_mx084htXKO1qbvovho1_500.gif', 'http://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif', 
		'http://25.media.tumblr.com/671f27962ca544ef8907ec0132c49ad1/tumblr_mp8srnNcTy1sx93aso1_500.gif', 'http://78.media.tumblr.com/tumblr_ma7l17EWnk1rq65rlo1_500.gif', 'https://m.imgur.com/8ruodNJ?r', 
		'https://myanimelist.cdn-dena.com/s/common/uploaded_files/1460993069-9ac8eaae8cd4149af4510d0fed0796bf.gif']

        #
        self.bite = ['https://media.giphy.com/media/pMT5VcMguh4Q0/giphy.gif', 'https://anime.aminoapps.com/page/blog/cute-bite-sweet-anime-girl-loli-big-eyes-kawai-lolicon/YMtb_u0GJaP06BMR2WReM3rKBVneYL', 
        'http://i.imgur.com/YCAzLzh.gif', 'https://78.media.tumblr.com/7e2cad3ab0432205cdd5c37fab83d977/tumblr_ojh7gzPyeB1uzwbyjo1_500.gif', 'https://media.tenor.com/videos/b6a549824362fc4f964b79d1d086b865/mp4', 
        'https://media1.tenor.com/images/a74770936aa6f1a766f9879b8bf1ec6b/tenor.gif', 'https://pa1.narvii.com/5965/95e6a157e606ce7e23fb4c7a7cd310c5f13d9d9a_hq.gif', 
        'https://vignette.wikia.nocookie.net/stevenuniverse-fanon/images/d/d1/Amethyst_bites_Pearl%27s_arm.gif/revision/latest?cb=20150513122650', 'http://i0.kym-cdn.com/photos/images/newsfeed/001/027/044/1cd.gif']

        #
        self.lewd =  ['http://i3.kym-cdn.com/photos/images/newsfeed/000/936/092/af7.jpg',  'http://i3.kym-cdn.com/photos/images/original/000/905/295/193.png', 
        'http://i3.kym-cdn.com/photos/images/original/000/897/703/b97.png', 'http://gallery.fanserviceftw.com/_images/a32b7d53651dcc3b76fcdc85a989c81b/9599%20-%20doushio%20makise_kurisu%20steins%3Bgate%20tagme.png', 
        'https://img.ifcdn.com/images/89ca6bd97bca8fabb4f3cb24f56e79b9ad020904e194f8cf99ff046d8da368a1_1.jpg', 'http://i2.kym-cdn.com/photos/images/newsfeed/000/888/789/f39.jpg', 'http://i1.kym-cdn.com/photos/images/original/000/988/917/ff8.jpg', 
        'http://i0.kym-cdn.com/photos/images/masonry/000/905/286/7ec.jpg','http://i1.kym-cdn.com/photos/images/facebook/000/794/434/6e7.gif']

        #
        self.kiss = ['http://media.giphy.com/media/FqBTvSNjNzeZG/giphy.gif', 'https://38.media.tumblr.com/d07fcdd5deb9d2cf1c8c44ffad04e274/tumblr_n2oqnslDSm1tv44eho1_500.gif', 'http://media.giphy.com/media/KmeIYo9IGBoGY/giphy.gif', 
        'http://25.media.tumblr.com/tumblr_mcf25oETLX1r0ydwlo1_500.gif', 'http://25.media.tumblr.com/tumblr_m88rxwNdCY1r6l8gpo1_500.gif', 'http://25.media.tumblr.com/ef9f2d6282f37026bff09f45757eda47/tumblr_mws4lpz9R41s3pk4mo1_500.gif#642927', 
        'http://media.giphy.com/media/kU586ictpGb0Q/giphy.gif', 'http://media.giphy.com/media/10i0tlqcYklEWY/giphy.gif', 'https://38.media.tumblr.com/bdea7d52f950d52e870c26d48a507481/tumblr_nq5xmrWkb21smg2oso1_500.gif', 
        'http://25.media.tumblr.com/f7bf9441a16b8837223a7f87ca16a0f1/tumblr_mga7rpNISY1rml571o1_500.gif', 'https://38.media.tumblr.com/6a0377e5cab1c8695f8f115b756187a8/tumblr_msbc5kC6uD1s9g6xgo1_500.gif', 
        'https://38.media.tumblr.com/54d820863ca93afd67460552bf0a01b8/tumblr_mmt5bk03k21so1hoto8_500.gif', 'http://25.media.tumblr.com/17e6890ca596eea98e00c86dfbadf0f6/tumblr_mz5gp8zQpO1sggrnxo1_500.gif', 
        'https://media.giphy.com/media/xTiTnKa9umn5skhyTK/giphy.gif', 'http://24.media.tumblr.com/b3d77735e349aefec4039e60eae51fd2/tumblr_mqc7j92TYp1rvkw6no1_500.gif', 
        'http://37.media.tumblr.com/6f8ff86f36a0c7fa6f6cf2b6c4b00663/tumblr_n4go91rApi1sfqkpto1_500.gif', 'http://geekparty.com/wp-content/uploads/2014/04/insta.gif', 'http://31.media.tumblr.com/tumblr_m3i48tDHTg1qefhtpo1_500.gif', 
        'http://i.imgur.com/xUF95bL.gif', 'http://31.media.tumblr.com/1e34fbdbfa86395d7adec1d3b675ba9b/tumblr_mxxdpuAoWU1slxwvro1_500.gif', 'http://s8.favim.com/orig/151119/akagami-no-shirayukihime-anime-boy-couple-Favim.com-3598058.gif',
        'https://em.wattpad.com/be664a8e8b471f49798ad367e7e809bea6dff987/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f5470763473634d653344323357413d3d2d3331373535353132392e3134373938323930393132363361666232353737353336373930322e676966?s=fit&w=1280&h=1280', 'http://fanserviceftw.com/gallery/_images/38ae1c6bd36796a463e3b916a066e264/5092%20-%20animated_gif%20hasegawa_haruka%20kiss%20moyashimon%20oikawa_hazuki%20yuri.gif', 
        'http://i.myniceprofile.com/1503/150305.gif', 'http://images6.fanpop.com/image/photos/36100000/yuri-image-yuri-36185616-300-169.gif', 'http://media.giphy.com/media/514rRMooEn8ti/giphy.gif', 
        'http://stream1.gifsoup.com/view1/1537307/anime-kiss-12-o.gif', 'http://37.media.tumblr.com/53bf74a951fc87a0cc15686f5aadb769/tumblr_n14rfuvCe41sc1kfto1_500.gif', 
        'http://24.media.tumblr.com/d4f03ca449e3d51325e9ba0cc6a11b24/tumblr_mmjr3zHgmw1s6qc3bo1_500.gif', 'https://media.giphy.com/media/tiML8HAwHkWDm/giphy.gif', 'http://cdn.awwni.me/n0eo.gif']

        #
        self.pickupline = ["Are you a tamale? ‘Cause you’re hot.",'You may fall from the sky, you may fall from a tree, but the best way to fall... is in love with me.', "Know what's on the menu? Me-n-u.", 
        "Guess what I'm wearing? The smile you gave me.", "Do you believe in love at first sight, or should I walk by again?", "Can I borrow a kiss? I promise I'll give it back.", 
        "If a fat man puts you in a bag at night, don't worry I told Santa I wanted you for Christmas.", "I'll be Burger King and you be McDonald's. I'll have it my way, and you'll be lovin' it.", 
        "You're so beautiful you made me forget my pick up line.", "I'm no photographer, but I can picture us together.", "Are you a parking ticket? Because you've got FINE written all over you.", 
        "Do I know you? Cause you look a lot like my next girlfriend.", "If I received a nickel for everytime I saw someone as beautiful as you, I'd have five cents.", 
        "Did you have lucky charms for breakfast? Because you look magically delicious!", "You are so sweet you could put Hershey's out of business.", "It's a good thing I wore my gloves today; otherwise, you'd be too hot to handle.", 
        "Did the sun come up or did you just smile at me?", "Was that an earthquake or did you just rock my world?", "You're so hot you must've started global warming.", "Damn girl, if you were a fruit, you'd be a FINEapple!", 
        "Excuse me, if I go straight this way, will I be able to reach your heart?", "I must be a snowflake, because I've fallen for you.", "Was your Dad a baker? Because you've got a nice set of buns.", 
        "We're like Little Ceasar's, we're Hot and Ready.", "Looks like you dropped something , My jaw!", "You are the reason Santa even has a naughty list.", "If I had a garden I'd put your two lips and my two lips together.", 
        "Do you have a mirror in your pocket? 'Cause I could see myself in your pants.", "Somebody call the cops, because it's got to be illegal to look that good!", "I'm not drunk, I'm just intoxicated by you.", 
        "If you were a laser you would be set on stunning.", "Could you please step away from the bar? You're melting all the ice!", "You must be a Snickers, because you satisfy me.", 
        "Can you take me to the bakery? Because, I want a Cutiepie like you!", "If you were a library book, I would check you out.", "Apart from being sexy, what do you do for a living?", 
        "I'm going to need a tall glass of cold water, cuz baby your making me HOT!", "What's your favorite silverware? Because I like to spoon!", "Baby, if you were words on a page, you’d be what they call fine print.", 
        "Can I get your picture to prove to all my friends that angels really do exist?", "Don’t walk into that building — the sprinklers might go off!", "Hey, I lost my phone number … Can I have yours?", 
        "Well, here I am. What are your other two wishes?", "Do you have a quarter? My mom told me to call her when I found the woman of my dreams.", "Do you have a band aid? I hurt my knee when I fell for you.",
         "The word of the day is legs. Let’s go back to my place and spread the word.", "You are so sweet you are giving me a toothache.", "Life without you would be like a broken pencil…pointless.", 
         "My magic watch says that you don’t have on any underwear. Oh..oh.. you, you do? \nDamn! it must be 15 minutes fast", "You turn my software into hardware!", "You must be in a wrong place – the Miss Universe contest is over there."]

        #
        self.ckiss = ['https://33.media.tumblr.com/b867332ef4f014a1c6da99d5bd29bebb/tumblr_n35yy0Udsw1qbvovho1_500.gif', 'http://i.imgur.com/QgfTZrS.gif', 'http://i.imgur.com/Z6V6mUE.mp4', 
        'http://orig00.deviantart.net/06a9/f/2015/054/a/a/cheekkainora_by_nikadonna-d8j8grg.gif', 'http://68.media.tumblr.com/2ced143e6bba445d359f982d0c3d659f/tumblr_n1ipntQonM1qbvovho8_500.gif', 
        'http://cdn.awwni.me/n3pg.gif', 'http://25.media.tumblr.com/3b8a73c70947679a6af56178762bdc1f/tumblr_mk8xzkenY71qzd219o1_500.gif', 'http://rs1099.pbsrc.com/albums/g399/Tantei-san/Conan-Kissonthecheek.gif~c200', 
        'https://i.giphy.com/media/12MEJ2ArZc23cY/source.gif', 'http://images6.fanpop.com/image/photos/32800000/Willis-kissing-Kari-and-Yolei-on-the-cheek-anime-32853445-500-250.gif', 
        'https://33.media.tumblr.com/90e09a6725fa20e59a69f2f7b2c4ad45/tumblr_n7wf3hH6rm1tv1jtto1_500.gif', 'http://data.whicdn.com/images/59643377/large.gif', 
        'https://38.media.tumblr.com/601f2d61d90e635968629bbb45a395e6/tumblr_nhd3g61Q6R1szhmk0o8_500.gif', 'http://www.lovethisgif.com/uploaded_images/5618-Anime-Kiss-Connect-Cheek-Kokoro-Animated-Gif.gif',
        'https://m.imgur.com/IVNTe32', 'https://thumbs.gfycat.com/ClearcutVainImperatorangel-max-1mb.gif', 'https://78.media.tumblr.com/043cadead20ea26375ef2730f9de736f/tumblr_o1ei0jcAZN1ufdoz0o1_500.gif']

        #
        self.pat = ['http://media.giphy.com/media/L2z7dnOduqEow/giphy.gif', 'http://33.media.tumblr.com/229ec0458891c4dcd847545c81e760a5/tumblr_mpfy232F4j1rxrpjzo1_r2_500.gif', 'https://media.giphy.com/media/12hvLuZ7uzvCvK/giphy.gif', 
        'http://i.imgur.com/eOJlnwP.gif', 'https://lh3.googleusercontent.com/-AGUIg-yZ5jE/VVUHX6vs6YI/AAAAAAAAIgA/d_kjvEtULJ0/w800-h450/Rikka.gif', 'http://pa1.narvii.com/5983/85777dd28aa87072ee5a9ed759ab0170b3c60992_hq.gif', 
        'https://media.giphy.com/media/xLm9fux5DSodq/giphy.gif', 'http://media.giphy.com/media/ye7OTQgwmVuVy/giphy.gif', 'http://37.media.tumblr.com/6c991608070a6056eb4390f9151d9c5e/tumblr_mprpthaR7f1rcag9ho1_500.gif', 
        'http://i.imgur.com/L8voKd1.gif', 'http://25.media.tumblr.com/tumblr_mckmheJJAZ1rqw7udo1_500.gif', 'http://33.media.tumblr.com/229ec0458891c4dcd847545c81e760a5/tumblr_mpfy232F4j1rxrpjzo1_r2_500.gif', 
        'http://24.media.tumblr.com/e6713de4cab8a28711835b6a339928b4/tumblr_mp0yr2VHQQ1rvdjx0o4_500.gif', 'https://33.media.tumblr.com/b8c4a62dc57062d7f9b16855a895ebe3/tumblr_mtg5mlcu0U1qbvovho1_500.gif', 
        'http://media.giphy.com/media/e7xQm1dtF9Zni/giphy.gif', 'http://25.media.tumblr.com/7026f9eba63fc60f8dbd7ba930dde430/tumblr_my4fqch4hS1qbvovho2_500.gif', 'http://i2.kym-cdn.com/photos/images/newsfeed/000/915/038/7e9.gif', 
        'http://25.media.tumblr.com/tumblr_m79ze5OKxk1rqon8do1_400.gif', 'https://media.giphy.com/media/igCbP09671uM0/giphy.gif', 'https://49.media.tumblr.com/fac1d9d768b722cec863b4172d10a765/tumblr_nbgidbQh9k1qbvovho1_500.gif', 
        'https://media.giphy.com/media/uw3fTCTNMbXAk/giphy.gif']


        #
        self.poke = ['http://31.media.tumblr.com/tumblr_lkn1twb83X1qbq4v6o1_500.gif',  'http://31.media.tumblr.com/tumblr_lkn1twb83X1qbq4v6o1_500.gif', 'https://media.giphy.com/media/psbjVYmRVfYJO/source.gif', 
        'http://orig01.deviantart.net/8acf/f/2011/328/a/d/fsn_saber_poke_attack_by_foreverirritated-d4h5hca.gif', 'http://38.media.tumblr.com/0809478d6759a0a4b431755026f677a0/tumblr_ntpfvoxeoz1u03j02o1_500.gif', 
        'http://media.tumblr.com/tumblr_mbcbgwzVfX1rwuydr.gif', 'http://i.imgur.com/rxsyBWA.jpg', 'http://s.myniceprofile.com/myspacepic/797/79743.gif', 'http://orig08.deviantart.net/03fe/f/2013/037/f/d/cry__poke_by_kiwa007-d5u29cm.gif', 
        'http://media.giphy.com/media/aZSMD7CpgU4Za/giphy.gif', 'https://media.giphy.com/media/y8p6B6bgKHlL2/giphy.gif', 'http://25.media.tumblr.com/a5ca5fcd9295bdbef4d78ddd0ecd42a1/tumblr_msk55wmNLi1ssbvp5o1_500.gif', 
        'http://i.amz.mshcdn.com/H2EYB0TAi-gRkULJQ6sX4qCQHrU=/fit-in/850x850/2014%2F02%2F21%2Fe5%2Fnemo.fb061.gif', 'http://orig00.deviantart.net/e55e/f/2012/323/b/5/itachi_and_sasuke_poke_by_endless_summer181-d5lhhet.gif', 
        'http://stream1.gifsoup.com/view1/2370407/undertaker-poke-o.gif', 'http://i.imgur.com/Ksw63.gif', 'http://orig04.deviantart.net/6a27/f/2011/197/b/a/cute___poke___nyan_by_ifmalover-d3weqc0.gif', 
        'http://www.gifwave.com/media/571143_anime-shut-up-clannad-poke-anime-funny.gif']

        #
        self.slap = ['http://orig11.deviantart.net/2d34/f/2013/339/1/2/golden_time_flower_slap_gif_by_paranoxias-d6wv007.gif', 'http://media.giphy.com/media/jLeyZWgtwgr2U/giphy.gif', 
        'http://rs1031.pbsrc.com/albums/y377/shinnidan/Toradora_-_Taiga_Slap.gif~c200', 'http://media.giphy.com/media/tMIWyF5GUrWwM/giphy.gif', 'http://www.animateit.net/data/media/243/aCC_AnimeAni2.gif', 
        'http://media.giphy.com/media/Zau0yrl17uzdK/giphy.gif', 'https://media.giphy.com/media/10Am8idu3qBYRy/giphy.gif', 
        'http://img-cache.cdn.gaiaonline.com/24f5017f9e5cb5a7c3a169a72d67c733/http://i797.photobucket.com/albums/yy257/MakeaLoves/Ryuuji%20n%20Taiga/Toradora_-_Taiga_Slap.gif', 
        'http://static1.wikia.nocookie.net/__cb20130131011839/adventuretimewithfinnandjake/images/c/cd/Slap.gif.gif', 'https://31.media.tumblr.com/dd5d751f86002fd4a544dcef7a9763d6/tumblr_inline_mya9hsvLZA1rbb2hd.gif', 
        'http://3.bp.blogspot.com/-CHYXl4bcgA0/UYGNzdDooBI/AAAAAAAADSY/MgmWVYn5ZR0/s400/2828+-+animated_gif+slap+umineko_no_naku_koro_ni+ushiromiya_maria+ushiromiya_rosa.gif', 'http://i.imgur.com/UXqzzab.gif', 
        'http://images6.fanpop.com/image/photos/32700000/Witch-slap-umineko-no-naku-koro-ni-32769187-500-283.gif', 'http://images2.fanpop.com/image/photos/9300000/Slap-Happy-futurama-9351667-352-240.gif', 
        'http://media.giphy.com/media/EpFsHUKK2MYvK/giphy.gif', 'http://ekladata.com/-vT5aTkK9ENUgyhqvNQfo7-Hids.gif', 'http://img.mrdrsr.net/slap.gif', 'http://fanaru.com/pandora-hearts/image/84052-pandora-hearts-pillow-slap.gif', 
        'https://media.giphy.com/media/XriT1FPiR1RRe/giphy.gif', 'http://i0.wp.com/haruhichan.com/wpblog/wp-content/uploads/Ryuuji-Takasu-x-Taiga-Aisaka-Toradora-anime-series-slap-haruhichan.com_.gif', 
        'https://media.giphy.com/media/1iw7RG8JbOmpq/giphy.gif', 'http://safebooru.org/images/363/5b1a06da49bd1eeccbf1f60428370c9b491b5156.gif?363332', 'https://artemisunfiltered.files.wordpress.com/2014/05/golden-time-nana-slap.gif', 
        'https://reallifeanime.files.wordpress.com/2014/06/akari-slap.gif', 'https://media.giphy.com/media/fNdolDfnVPKNi/giphy.gif', 'http://media.tumblr.com/tumblr_lx84j9KIBZ1qg12e8.gif',
        'http://img.wonkette.com/wp-content/uploads/2013/07/107815-animated-animation-artist3asubjectnumber2394-fight-gif-sissy_slap_fight-trixie-twilight_sparkle.gif']

        #
        self.lewd =  ['http://i3.kym-cdn.com/photos/images/newsfeed/000/936/092/af7.jpg', 'http://i.imgur.com/tkEOnku.jpg', 'http://i3.kym-cdn.com/photos/images/original/000/905/295/193.png', 'http://i.imgur.com/Kscx9g5.png', 
        'http://i3.kym-cdn.com/photos/images/original/000/897/703/b97.png', 'http://gallery.fanserviceftw.com/_images/a32b7d53651dcc3b76fcdc85a989c81b/9599%20-%20doushio%20makise_kurisu%20steins%3Bgate%20tagme.png', 
        'https://img.ifcdn.com/images/89ca6bd97bca8fabb4f3cb24f56e79b9ad020904e194f8cf99ff046d8da368a1_1.jpg', 'http://i2.kym-cdn.com/photos/images/newsfeed/000/888/789/f39.jpg', 'http://i1.kym-cdn.com/photos/images/original/000/988/917/ff8.jpg', 
        'http://i0.kym-cdn.com/photos/images/masonry/000/905/286/7ec.jpg','http://i1.kym-cdn.com/photos/images/facebook/000/794/434/6e7.gif']

        #
        self.cuddle = ['http://media.giphy.com/media/QlFyrikSI01Fe/giphy.gif', 'http://media.tumblr.com/01949fb828854480b513a87fa4e8eee7/tumblr_inline_n5r8vyJZa61qc7mf8.gif', 'http://media.giphy.com/media/Ki88u2LhvDhyE/giphy.gif', 
        'http://www.ohmagif.com/wp-content/uploads/2012/07/cute-puppy-cuddling-with-cat.gif', 'http://awesomegifs.com/wp-content/uploads/cat-and-dog-cuddling.gif', 'http://big.assets.huffingtonpost.com/cuddlecat.gif', 
        'http://25.media.tumblr.com/d9f3e83abe3e01d1174dae0a771750cd/tumblr_mi4ll7Rqqe1rqszceo1_400.gif', 'https://lh3.googleusercontent.com/-H8YQfmNXcus/UNH4jtH3gkI/AAAAAAAAGpA/FHslZSXRs6I/s233/141.gif', 
        'https://media.giphy.com/media/ipTpDF6TOdgc/giphy.gif', 'https://media.giphy.com/media/ztXa20eZi18oo/giphy.gif', 'http://www.rinchupeco.com/wp-content/uploads/2013/06/cuddle.gif', 
        'http://s2.favim.com/orig/36/ash-bed-hug-pikachu-pokemon-Favim.com-295600.gif']

        #
        self.snuggle = ['http://media.giphy.com/media/QlFyrikSI01Fe/giphy.gif', 'http://media.tumblr.com/01949fb828854480b513a87fa4e8eee7/tumblr_inline_n5r8vyJZa61qc7mf8.gif', 'http://media.giphy.com/media/Ki88u2LhvDhyE/giphy.gif', 
        'http://www.ohmagif.com/wp-content/uploads/2012/07/cute-puppy-cuddling-with-cat.gif', 'http://awesomegifs.com/wp-content/uploads/cat-and-dog-cuddling.gif', 'http://big.assets.huffingtonpost.com/cuddlecat.gif', 
        'http://25.media.tumblr.com/d9f3e83abe3e01d1174dae0a771750cd/tumblr_mi4ll7Rqqe1rqszceo1_400.gif', 'https://lh3.googleusercontent.com/-H8YQfmNXcus/UNH4jtH3gkI/AAAAAAAAGpA/FHslZSXRs6I/s233/141.gif', 
        'https://media.giphy.com/media/ipTpDF6TOdgc/giphy.gif', 'https://media.giphy.com/media/ztXa20eZi18oo/giphy.gif', 'http://www.rinchupeco.com/wp-content/uploads/2013/06/cuddle.gif', 
        'http://s2.favim.com/orig/36/ash-bed-hug-pikachu-pokemon-Favim.com-295600.gif']

        #
        self.punch = ['https://media.tenor.co/images/c22ccca9bccec97234cfa3f0147c32a9/raw', 'https://media.giphy.com/media/11zD6xIdX4UOfS/giphy.gif', 'https://media.tenor.co/images/c119c32b931abd9c9d6471839d0e35f2/raw', 
        'http://media3.giphy.com/media/LdsJrFnANh6HS/giphy.gif', 'http://media.giphy.com/media/mLn5AIQK2WEwg/giphy.gif', 'https://media.tenor.co/images/9117e543eb665a49ae73fd960c5f7d57/raw', 
        'https://media.giphy.com/media/Z5zuypybI5dYc/giphy.gif', 'https://media.giphy.com/media/10Im1VWMHQYfQI/giphy.gif', 'http://24.media.tumblr.com/tumblr_llzoy4WqVw1qd9kxeo1_500.gif', 'http://i.imgur.com/t7UzKxg.gif', 
        'http://ohn1.slausworks.netdna-cdn.com/newohnblog/wp-content/uploads/2013/09/punch_anime.gif']

        #
        self.sob =  ['http://24.media.tumblr.com/b7ae6c694085e0b294cdd938278c70c7/tumblr_mpupx1krXM1s3jc4vo1_400.gif', 'http://media.giphy.com/media/ZlWplgoWyskQo/giphy.gif', 
        'http://mrwgifs.com/wp-content/uploads/2013/05/Dramatic-Crying-In-Anime-Gif.gif', 'http://24.media.tumblr.com/4b53f4cf45e7f72910ca5120f19a8aa8/tumblr_mnzdt6fGen1s645eto1_500.gif', 
        'https://38.media.tumblr.com/b6d6e61e7adb56ab4283c9f96fe67163/tumblr_mqvjmqrMqs1spu46io1_500.gif', 'http://gif-finder.com/wp-content/uploads/2015/07/Anime-girl-crying.gif', 
        'https://s-media-cache-ak0.pinimg.com/originals/69/fc/82/69fc828893e612d86fc7bb85862be96e.gif', 'http://25.media.tumblr.com/c65a4af4ff032d1ca06350b66a1e819c/tumblr_mtxk6zVzaa1sogk1do1_r1_500.gif', 
        'http://media.giphy.com/media/ROF8OQvDmxytW/giphy.gif', 'http://media.giphy.com/media/QUKkvRTIYLgMo/giphy.gif', 'http://media.tumblr.com/tumblr_mdaindozZF1ryvbtl.gif', 
        'https://31.media.tumblr.com/b307cca19d29eb1625bd841e661c0f59/tumblr_mvjhgmknl91stfs7go1_500.gif', 'http://media1.giphy.com/media/4pk6ba2LUEMi4/giphy.gif']

    @commands.command(name="8ball")
    async def eightballcmd(self, ctx, *, question: str):
        messages = ['It is certain',
            'It is decidedly so',
            'Yes definitely',
            'Reply hazy, try again',
            'Ask again later',
            'Concentrate and ask again',
            'My reply is no',
            'Outlook not so good',
            'Very doubtful']
        result = random.choice(messages)
        emb = Embeds.create_embed(self, ctx, title=question, color=0x00aaff, message=result)
        await ctx.send(embed=emb)

    @commands.command(name="lick")
    async def lickcmd(self, ctx, user=None):
        result = random.choice(self.lick)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Licking {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="hug")
    async def hugcmd(self, ctx, user=None):
        result = random.choice(self.hug)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Hugging {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="bite")
    async def bitecmd(self, ctx, user=None):
        result = random.choice(self.bite)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Biting {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="kiss")
    async def kisscmd(self, ctx, user=None):
        result = random.choice(self.kiss)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Kissing {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="ckiss")
    async def ckisscmd(self, ctx, user=None):
        result = random.choice(self.ckiss)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Kissing {} on the cheek".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="cuddle")
    async def cuddlecmd(self, ctx, user=None):
        result = random.choice(self.cuddle)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Cuddling with {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="snuggle")
    async def snugglecmd(self, ctx, user=None):
        result = random.choice(self.snuggle)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Snuggled up with {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="slap")
    async def slapcmd(self, ctx, user=None):
        result = random.choice(self.slap)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Slapping {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="lewd")
    async def lewdcmd(self, ctx, user=None):
        result = random.choice(self.lewd)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Lewding {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="punch")
    async def punchcmd(self, ctx, user=None):
        result = random.choice(self.punch)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Punching {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="poke")
    async def pokecmd(self, ctx, user=None):
        result = random.choice(self.poke)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Poking {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="pat")
    async def patcmd(self, ctx, user=None):
        result = random.choice(self.pat)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Patting {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="flirt")
    async def flirtcmd(self, ctx, user=None):
        result = random.choice(self.pickupline)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Flirting with {}".format(user), result)
        await ctx.send(emed=emb)

    @commands.command(name="sob")
    async def sobcmd(self, ctx, user=None):
        result = random.choice(self.sob)
        if user:
            pass
        else:
            user = ctx.message.author.name
        emb = Embeds.create_embed(self, ctx, "Sobbing because of {}".format(user), 0x00aaff)
        emb.set_image(url=result)
        await ctx.send(embed=emb)

    @commands.command(name="rate")
    async def ratecmd(self, ctx, user):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        rating = random.choice(numbers)
        emb = Embeds.create_embed(self, ctx, "Waifu Rating", 0xaaff, "{}\n{}/10".format(user, rating))
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Fun(bot))