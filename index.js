const menu = document.getElementById("menu");

Array.from(document.getElementsByClassName("menu-item"))
  .forEach((item, index) => {
    item.onmouseover = () => {
      menu.dataset.activeIndex = index;
    }
  });

  $(document).ready(function() {
    $(".menu-item").click(function(event) {
      event.preventDefault(); // Prevent the default behavior of the anchor tag

      var targetId = $(this).attr("href"); // Get the ID of the target div from the href attribute
      var targetPosition = $(targetId).offset().top; // Get the position of the target div relative to the top of the page

      $("html, body").animate(
        {
          scrollTop: targetPosition // Scroll smoothly to the target div
        },
        1000, // The duration of the animation in milliseconds (adjust as needed)
        function() {
          // After the scrolling animation is complete, update the URL hash to allow back-button functionality
          window.location.hash = targetId;
        }
      );
    });

    // Check for hash change (when user presses back/forward button)
    $(window).on('hashchange', function() {
      var targetId = window.location.hash;
      var targetPosition = $(targetId).offset().top;

      $("html, body").animate(
        {
          scrollTop: targetPosition
        },
        1000 // The duration of the animation in milliseconds (adjust as needed)
      );
    });
  });

