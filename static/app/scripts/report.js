// ----------------------------
// Data Explorer
// ----------------------------

function reportN1Headers() {
    $.getJSON("report_n1_headers", function (data) {
        $.each(data, function (key, val) {
            app._data.head_more_restrictive_items.push(val);
        });

    });
}

function reportN2Headers() {
    $.getJSON("report_n2_headers", function (data) {
        $.each(data, function (key, val) {
            app._data.head_less_restrictive_items.push(val);
        });

    });
}

function reportN1Items() {
    $.getJSON("report_n1_items", function (data) {
        $.each(data, function (key, val) {
            app._data.rp_n1_items.push(val);
        });

    });
}

function reportN2Items() {
    $.getJSON("report_n2_items", function (data) {
        $.each(data, function (key, val) {
            app._data.rp_n2_items.push(val);
        });

    });
}

reportN1Headers();
reportN2Headers();
reportN1Items();
reportN2Items();