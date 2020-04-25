  const answer = (chosen) => {
        console.log(chosen);
        fadeOut(document.getElementById("quiz"),500);
        let xhr = new XMLHttpRequest();
        xhr.open('GET', `/reply/${chosen}`);
        xhr.onreadystatechange = function() {
            window.location = `/?random=${Math.round(Math.random()*1000)}`;
        };
        xhr.send();
    };

    const showTime = async () => {
        result = await fetch("/time_left");
        document.getElementById("time_left").innerHTML = await result.text();
    };

    showTime();

    setInterval(async ()=> {
        showTime();
    }, 5000);

    function fadeIn(elem, ms) {
        if (!elem)
            return;

        elem.style.opacity = 0;
        elem.style.filter = "alpha(opacity=0)";
        elem.style.display = "inline-block";
        elem.style.visibility = "visible";

        if (ms) {
            var opacity = 0;
            var timer = setInterval(function () {
                opacity += 50 / ms;
                if (opacity >= 1) {
                    clearInterval(timer);
                    opacity = 1;
                }
                elem.style.opacity = opacity;
                elem.style.filter = "alpha(opacity=" + opacity * 100 + ")";
            }, 50);
        } else {
            elem.style.opacity = 1;
            elem.style.filter = "alpha(opacity=1)";
        }
    }

    function fadeOut(elem, ms) {
        if (!elem)
            return;

        if (ms) {
            var opacity = 1;
            var timer = setInterval(function () {
                opacity -= 50 / ms;
                if (opacity <= 0) {
                    clearInterval(timer);
                    opacity = 0;
                    elem.style.display = "none";
                    elem.style.visibility = "hidden";
                }
                elem.style.opacity = opacity;
                elem.style.filter = "alpha(opacity=" + opacity * 100 + ")";
            }, 50);
        } else {
            elem.style.opacity = 0;
            elem.style.filter = "alpha(opacity=0)";
            elem.style.display = "none";
            elem.style.visibility = "hidden";
        }
    }
