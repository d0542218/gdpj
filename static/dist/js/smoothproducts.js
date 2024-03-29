/*
 * Smoothproducts version 2.0.2
 * http://kthornbloom.com/smoothproducts.php
 *
 * Copyright 2013, Kevin Thornbloom
 * Free to use and abuse under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 */

 (function($) {
 	$.fn.extend({
 		deleteSmoothProducts: function () {
 			$(document.body).off('click', '.sp-lightbox');
 			$(document.body).off('click', '#sp-prev');
 			$(document.body).off('click', '#sp-next');
 			$(document.body).off('click', '.sp-large a');
 			$(document.body).off('click', '.sp-noff-touch .sp-zoom');
 			$(document.body).off('click', '.sp-tb-active a');
 			$(document.body).off('click', '.sp-thumbs');
 		},
 		smoothproducts: function(productId) {
 			var i =1;
			// Add some markup & set some CSS
			$('.sp-loading').hide();
			$(productId).each(function() {
				$(this).addClass('sp-touch');
				var thumbQty = $('a', this).length;

				// If more than one image
				if (thumbQty > 1) {
					var firstLarge,firstThumb,
					defaultImage = $('a.sp-default', this)[0]?true:false;
					if(productId=='#step2-wrap'){					
						$(this).append('<div class="sp-large"></div><div id="items-list" class="sp-thumbs sp-tb-active"></div>');
					}else{
						$(this).append('<div class="sp-large"></div><div class="sp-thumbs sp-tb-active"></div>');
					}
					$('a', this).each(function(index) {
						var thumb = $('img', this).attr('src'),
						large = $(this).attr('href'),
						classes = '';
						//set default image
						if((index === 0 && !defaultImage) || $(this).hasClass('sp-default')){
							classes = ' class="sp-current"';
							firstLarge = large;
							firstThumb = $('img', this)[0].src;
						}
						if(productId=='#step2-wrap'){
							$(this).parents(productId).find('.sp-thumbs').append('<a id="'+i+'" href="' + large + '" style="background-image:url(' + thumb + ')"'+classes+'></a>');
							i+=1;
						}else{
							$(this).parents(productId).find('.sp-thumbs').append('<a href="' + large + '" style="background-image:url(' + thumb + ')"'+classes+'></a>');
						}
						$(this).remove();
					});
					if(productId=='#step3-content1'){
						$('.sp-large').attr('max-height','842px');
					}
					$('.sp-large', this).append('<a href="' + firstLarge + '" class="sp-current-big"><img src="' + firstThumb + '" alt="" id ="sp-current-big-img"/></a>');
					$(productId).css('display', 'inline-block');
				// If only one image
			} else {
				$(this).append('<div class="sp-large"></div>');
				$('a', this).appendTo($('.sp-large', this)).addClass('sp-current-big');
				$('img', this).attr('id','sp-current-big-img');
				$(productId).css('display', 'inline-block');
			}
		});


			// Prevent clicking while things are happening
			$(document.body).on('click', '.sp-thumbs', function(event) {
				event.preventDefault();
			});


			// Is this a touch screen or not?
			$(document.body).on('mouseover', function(event) {
				$(productId).removeClass('sp-touch').addClass('sp-non-touch');
				event.preventDefault();
			});

			$(document.body).on('touchstart', function() {
				$(productId).removeClass('sp-non-touch').addClass('sp-touch');
			});

			// Clicking a thumbnail
			$(document.body).on('click', '.sp-tb-active a', function(event) {

				event.preventDefault();
				$(this).parent().find('.sp-current').removeClass();
				$(this).addClass('sp-current');
				$(this).parents(productId).find('.sp-thumbs').removeClass('sp-tb-active');
				$(this).parents(productId).find('.sp-zoom').remove();

				var currentHeight = $(this).parents(productId).find('.sp-large').height(),
				currentWidth = $(this).parents(productId).find('.sp-large').width();
				$(this).parents(productId).find('.sp-large').css({
					overflow: 'hidden',
					height: currentHeight + 'px',
					width: currentWidth + 'px'
				});

				$(this).addClass('sp-current').parents(productId).find('.sp-large a').remove();

				var nextLarge = $(this).parent().find('.sp-current').attr('href'),
				nextThumb = get_url_from_background($(this).parent().find('.sp-current').css('backgroundImage'));

				$(this).parents(productId).find('.sp-large').html('<a href="' + nextLarge + '" class="sp-current-big"><img src="' + nextThumb + '" id ="sp-current-big-img"/></a>');
				$(this).parents(productId).find('.sp-large').hide().fadeIn(250, function() {

					var autoHeight = $(this).parents(productId).find('.sp-large img').height();

					$(this).parents(productId).find('.sp-large').animate({
						height: autoHeight
					}, 'fast', function() {
						$('.sp-large').css({
							height: 'auto',
							width: 'auto'
						});
					});

					$(this).parents(productId).find('.sp-thumbs').addClass('sp-tb-active');
				});
			});

			// Zoom In non-touch
			// $(document.body).on('mouseenter', '.sp-non-touch .sp-large', function(event) {
			// 	var largeUrl = $('a', this).attr('href');
			// 	$(this).append('<div class="sp-zoom"><img src="' + largeUrl + '"/></div>');
			// 	$(this).find('.sp-zoom').fadeIn(250);
			// 	event.preventDefault();
			// });

			// // Zoom Out non-touch
			// $(document.body).on('mouseleave', '.sp-non-touch .sp-large', function(event) {
			// 	$(this).find('.sp-zoom').fadeOut(250, function() {
			// 		$(this).remove();
			// 	});
			// 	event.preventDefault();
			// });

			// Open in Lightbox non-touch
			// Open in Lightbox non-touch
			$(document.body).on('click', '.sp-non-touch .sp-zoom', function(event) {
				var currentImg = $(this).html(),
				thumbAmt = $(this).parents(productId).find('.sp-thumbs a').length,
				currentThumb = ($(this).parents(productId).find('.sp-thumbs .sp-current').index())+1;
				$(this).parents(productId).addClass('sp-selected');
				$('body').append("<div class='sp-lightbox' data-currenteq='"+currentThumb+"'>" + currentImg + "</div>");

				if(thumbAmt > 1){
					$('.sp-lightbox').append("<a href='#' id='sp-prev'></a><a href='#' id='sp-next'></a>");
					if(currentThumb == 1) {
						$('#sp-prev').css('opacity','.1');
					} else if (currentThumb == thumbAmt){
						$('#sp-next').css('opacity','.1');
					}
				}
				$('.sp-lightbox').fadeIn();
				event.preventDefault();
			});

			// Open in Lightbox touch
			$(document.body).on('click', '.sp-large a', function(event) {
				var currentImg = $(this).attr('href'),
				thumbAmt = $(this).parents(productId).find('.sp-thumbs a').length,
				currentThumb = ($(this).parents(productId).find('.sp-thumbs .sp-current').index())+1;

				$(this).parents(productId).addClass('sp-selected');
				$('body').append('<div class="sp-lightbox" data-currenteq="'+currentThumb+'"><img src="' + currentImg + '"/></div>');

				if(thumbAmt > 1){
					$('.sp-lightbox').append("<a href='#' id='sp-prev'></a><a href='#' id='sp-next'></a>");
					if(currentThumb == 1) {
						$('#sp-prev').css('opacity','.1');
					} else if (currentThumb == thumbAmt){
						$('#sp-next').css('opacity','.1');
					}
				}
				$('.sp-lightbox').fadeIn();
				event.preventDefault();
			});

			// Pagination Forward
			$(document.body).on('click', '#sp-next', function(event) {
				event.stopPropagation();
				var currentEq = $('.sp-lightbox').data('currenteq'),
				totalItems = $('.sp-selected .sp-thumbs a').length;

				if(currentEq >= totalItems) {
				} else {
					var nextEq = currentEq + 1,
					newImg = $('.sp-selected .sp-thumbs').find('a:eq('+currentEq+')').attr('href'),
					newThumb = get_url_from_background($('.sp-selected .sp-thumbs').find('a:eq('+currentEq+')').css('backgroundImage'));
					if (currentEq == (totalItems - 1)) {
						$('#sp-next').css('opacity','.1');
					}
					$('#sp-prev').css('opacity','1');
					$('.sp-selected .sp-current').removeClass();
					$('.sp-selected .sp-thumbs a:eq('+currentEq+')').addClass('sp-current');
					$('.sp-selected .sp-large').empty().append('<a href='+newImg+'><img src="'+newThumb+'"/></a>');
					$('.sp-lightbox img').fadeOut(250, function() {
						$(this).remove();
						$('.sp-lightbox').data('currenteq',nextEq).append('<img src="'+newImg+'"/>');
						$('.sp-lightbox img').hide().fadeIn(250);
					});
				}

				event.preventDefault();
			});

		// Pagination Backward
		$(document.body).on('click', '#sp-prev', function(event) {

			event.stopPropagation();
			var currentEq = $('.sp-lightbox').data('currenteq'),
			currentEq = currentEq - 1;
			if(currentEq <= 0) {
			} else {
				if (currentEq == 1) {
					$('#sp-prev').css('opacity','.1');
				}
				var nextEq = currentEq - 1,
				newImg = $('.sp-selected .sp-thumbs').find('a:eq('+nextEq+')').attr('href'),
				newThumb = get_url_from_background($('.sp-selected .sp-thumbs').find('a:eq('+nextEq+')').css('backgroundImage'));
				$('#sp-next').css('opacity','1');
				$('.sp-selected .sp-current').removeClass();
				$('.sp-selected .sp-thumbs a:eq('+nextEq+')').addClass('sp-current');
				$('.sp-selected .sp-large').empty().append('<a href='+newImg+'><img src="'+newThumb+'"/></a>');
				$('.sp-lightbox img').fadeOut(250, function() {
					$(this).remove();
					$('.sp-lightbox').data('currenteq',currentEq).append('<img src="'+newImg+'"/>');
					$('.sp-lightbox img').hide().fadeIn(250);
				});
			}
			event.preventDefault();
		});


			// Close Lightbox
			$(document.body).on('click', '.sp-lightbox', function() {
				closeModal();
			});

			// Close on Esc
			$(document).keydown(function(e) {
				if (e.keyCode == 27) {
					closeModal();
					return false;
				}
			});

			function closeModal (){
				$('.sp-selected').removeClass('sp-selected');
				$('.sp-lightbox').fadeOut(function() {
					$(this).remove();
				});
			}
			function get_url_from_background(bg){
				return bg.match(/url\([\"\']{0,1}(.+)[\"\']{0,1}\)+/i)[1];
			}
			let items = document.querySelectorAll('#items-list > a')
			items.forEach(item => {
				$(item).prop('draggable', true)
				item.addEventListener('dragstart', dragStart)
				item.addEventListener('drop', dropped)
				item.addEventListener('dragenter', cancelDefault)
				item.addEventListener('dragover', cancelDefault)
			})
			function dragStart (e) {
				var index = $(e.target).index();
				e.dataTransfer.setData('text/plain', index);
			}
			function dropped (e) {
				cancelDefault(e)
				  // get new and old index
				  let oldIndex = e.dataTransfer.getData('text/plain')
				  let target = $(e.target)
				  let newIndex = target.index()
				  // remove dropped items at old place
				  let dropped = $(this).parent().children().eq(oldIndex).remove()
				  // insert the dropped items at new place
				  if (newIndex < oldIndex) {
				  	target.before(dropped)
				  } else {
				  	target.after(dropped)
				  }
				}
				function cancelDefault (e) {
					e.preventDefault()
					e.stopPropagation()
					return false
				}
			}
		});
})(jQuery);
