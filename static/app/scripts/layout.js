// ----------------------------
// Local Variables
// ----------------------------

_page_index = 1
_scroll_tolerance = 3
_items = []

function removeFromArray(arr) {
    var what, a = arguments, L = a.length, ax;
    while (L > 1 && arr.length) {
        what = a[--L];
        while ((ax = arr.indexOf(what)) !== -1) {
            arr.splice(ax, 1);
        }
    }
    return arr;
}


// ----------------------------
// Vue
// ----------------------------
let app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    /* mounted () {
        /* eslint-disable no-new */
    //    new Sortable (
    //      this.$refs.sortableTable.$el.getElementsByTagName('tbody')[0],
    //      {
    //        draggable: '.sortableRow',
    //        handle: '.sortHandle',
    //        onEnd: this.dragReorder
    //      }
    //    )
    //  },
    data() {
        return {
            offsetTop: 0,
            dialogComment: false,
            dialogfilter: false,
            dialogCatalogsModel: false,
            dialogProcessFinished: false,
            dialogProcessStarted: false,
            catalogDialogHeaders: [
                {text: 'Name', value: 'catalogName', align: 'left', sortable: false},
                {text: 'Version', value: 'catalogVersion', align: 'left', sortable: false}
            ],
            catalogDialogItems: [],
            catalogDialogSearch: '',
            filterchips: [],
            rowMainArray: [],
            drawer: true,
            rightDrawer: false,
            filterButtonLabel: 'OPEN FILTERS',
            modelSelectRestrictivity: [],
            itemsSelectRestrictivity: [
                {text: 'More Restrictive: Considering Attributes', value: 1},
                {text: 'Less Restrictive: Disregarding Attributes', value: 2},
			],
			headers: [
                // HEADER VIA VAREJO
                
                //{ text: 'SKU', value: 'IdSKU', align: 'left', sortable: false },
                //{ text: 'NAME', value: 'Product_Name', align: 'left', sortable: false, },
                //{ text: 'PARTNER_NAME', value: 'Partner_Name', align: 'left', sortable: false, },
                //{ text: 'ATTRIBUTE', value: 'Main_Attribute', align: 'left', sortable: false, },
                //{ text: 'GTIN', value: 'GTIN', align: 'left', sortable: false, },
                //{ text: 'BRAND', value: 'Brand_Name', align: 'left', sortable: false, },
                //{ text: 'CATEGORY_1', value: 'Category_Name_1', align: 'left', sortable: false, },
                //{ text: 'CATEGORY_2', value: 'Category_Name_1', align: 'left', sortable: false, },
            
                
                // HEADER DOTZ
                /*
                { text: 'PARTNER_ID', value: 'PARTNER_ID', align: 'left', sortable: false },
				{ text: 'NAME', value: 'NAME', align: 'left', sortable: false, },
				{ text: 'GTIN', value: 'GTIN', align: 'left', sortable: false, },
				{ text: 'BRAND', value: 'BRAND', align: 'left', sortable: false, },
				{ text: 'CATEGORY_1', value: 'CATEGORY_1', align: 'left', sortable: false, },
				{ text: 'CATEGORY_2', value: 'CATEGORY_2', align: 'left', sortable: false, },
                */

                //{text: '# COUNT', value: 'count', align: 'right', sortable: false,},
                //{text: 'ACTIONS', value: 'ACTIONS', align: 'right', sortable: false,},
            ],
            items: [],
            fcategory1: [],
            fcategory2: [],
            fcategory3: [],
            fbrand: [],
            fgroup: [],
            mfcategory1: [],
            mfcategory2: [],
            mfcategory3: [],
            mfbrand: [],
            mfgroup: [],
            mtxtsearch: "",
            loading: false,
            inputCommentModel: "",
            selectedItemModel: "",
            dialogloading: false,
            pages: 0,
            page: 0,
            itemsquantitypage: [],
            modelquantitypage: [],
            filters: 0,
            headers_rep_n1: [
                {text: 'Group', value: 'GROUP', align: 'center',},
                {text: 'Products', value: 'QT_NAME', align: 'center',},
                {text: 'Clusters', value: 'QT_CLUSTER', align: 'center',},
                {text: '%', value: 'PC_CLUSTER', align: 'center',}
            ],
            rp_n1_headers: [],
            rp_n2_headers: [],
            rp_n1_items: [],
            rp_n2_items: [],
            graph_data: [],
            combo_report: [{
                item: 'More Restrictive - Considering Attributes',
                value: 1
            }, {item: 'Less Restrictive - Disregarding Attributes', value: 2}],
            model_combo_report: [],
            head_statistics_items: [
                { text: 'Detail Level', value: 1 },
                { text: '# Total Itens', value: 2 },
                { text: '# Total Itens Transformed', value: 3 },
                { text: '# Total Clusters', value: 4 },
                { text: '# Clusters: Duplicated', value: 5 },
                { text: '# Clusters: Uniques', value: 6 },
                { text: '# Itens: Duplicated', value: 7 },
                { text: '# Itens: Uniques', value: 8 },
                { text: '% Itens Clusterized', value: 9 },
                { text: '# Partners Involved', value: 10 }
            ],
            head_interacted_items: [
                { text: 'Interacted Itens', value: 1 },
                { text: '# Clusters: Row Main Changed', value: 2 },
                { text: '# Itens Removed from Cluster', value: 3 },
                { text: '# Itens Tagged', value: 4 }
            ],
            head_more_restrictive_items: [],
            head_less_restrictive_items: [],
            cards: [
                {title: 'Catalog Info', flex: 6},
                {title: 'Statistics', flex: 6},
                {title: '3D Graphic Visualization', flex: 6},
                {title: 'Catalog Versions', flex: 6},
            ],
            catalogInfo: [],
            statisticsInfo: [],
            valid: true,
            userRules: [
                (v) => !!v || 'User is required',
                (v) => v && v.length > 3 || 'Name must have more then 3 characters'
            ],
            passwordRules: [
                (v) => !!v || 'Password is required',
                (v) => v && v.length > 7 || 'Password must have at least 8 characters'
            ],
            userModel: '',
            passwordModel: '',
            errorLogin: "",
            errorAlert: false,
            e3: true,
            canProcess: false,
            canPublish: false,
        }
    },
    created: function () {
        this.catalogDialogItems = [];
        let array_internal = [];

        /*
        COMMENTED TO FUTURE USE
        $.getJSON("list_catalogs", function (data) {
            $.each(data, function (key, val) {
                array_internal.push(val);
            });
        });

        this.catalogDialogItems = array_internal;*/

        window.addEventListener('keyup', function (e) {
            if ((e.keyCode || e.which) == 13) {
                watchEnter();
            } else {
                if ((e.keyCode || e.which) == 27) {
                    let pathname = window.location.pathname;

                    if (pathname === "/") {
                        watchEsc();
                    }
                }
            }
        }, true);

        $.getJSON("get_statistics_info", function (data) {
            app._data.statisticsInfo = data;
        });
    },
    watch: {
        page() {
            loadPage(this.filters, this.page);
        },
        mfgroup() {
            setFilter('mfgroup', this.mfgroup);
        },
        mfbrand() {
            setFilter('mfbrand', this.mfbrand);
        },
        mfcategory1() {
            setFilter('mfcategory1', this.mfcategory1);
        },
        mfcategory2() {
            setFilter('mfcategory2', this.mfcategory2);
        },
        mfcategory3() {
            setFilter('mfcategory3', this.mfcategory3);
        },
        modelquantitypage() {
            setQuantityPerPage(this.modelquantitypage);
        },
        filterchips() {
            if (this.filterchips.length == 0) {
                this.clearAll();
            }
        },
        rightDrawer() {
            this.filterButtonLabel = "OPEN FILTERS";
            if (this.rightDrawer) {
                this.filterButtonLabel = "CLOSE FILTERS";
            }
        },
        errorAlert() {
            if (this.errorAlert) {
                setTimeout(function () {
                    app._data.errorAlert = false;
                }, 3000);
            }
        }
    },
    methods: {
        dragReorder ({oldIndex, newIndex}) {
            const movedItem = this.items.splice(oldIndex, 1)[0]
            this.items.splice(newIndex, 0, movedItem)
        },
        itemKey (item) {
            if (!this.itemKeys.has(item)) this.itemKeys.set(item, ++this.currentItemKey)
            return this.itemKeys.get(item)
        },

        classChanger(rowmain, wrong, alignment) {
            let viewclass = false;
            let alignleft = false;
            let alignright = false;
            let viewwrong = false;

            if (alignment == 1) {
                alignleft = true;
                alignright = false;
            } else {
                alignleft = false;
                alignright = true;
            }

            if (rowmain == 1) {
                viewclass = true;
            }

            if (wrong == '1') {
                viewclass = false;
                viewwrong = true;
            }

            return {
                'blue lighten-4': viewclass,
                'red lighten-5': viewwrong,
                'text-xs-left': alignleft,
                'text-xs-right': alignright,
            }
        },
        removechip(item) {
            this.filterchips.splice(this.filterchips.indexOf(item), 1);
            this.filterchips = [...this.filterchips];
        },
        toggleAll() {
            if (this.selected.length) {
                this.selected = [];
            }
            else {
                this.selected = this.items[1].slice();
            }
        },
        changeSort(column) {
            if (this.pagination.sortBy === column) {
                this.pagination.descending = !this.pagination.descending;
            } else {
                this.pagination.sortBy = column;
                this.pagination.descending = false;
            }
        },
        updateComment() {
            setComment();
        },
        setButtonColor(button_id, answer) {
            if ($("#" + button_id).css('color') == "rgb(0, 0, 0)" && answer == 0) {
                $("#" + button_id).css('color', 'rgb(0, 128, 0)');
            } else {
                if ($("#" + button_id).css('color') == "rgb(0, 0, 0)" && answer == 1) {
                    $("#" + button_id).css('color', 'rgb(255, 0, 0)');
                } else {
                    if ($("#" + button_id).css('color') == "rgb(0, 128, 0)" && answer == 0) {
                        $("#" + button_id).css('color', 'rgb(0, 0, 0)');
                    } else {
                        $("#" + button_id).css('color', 'rgb(0, 0, 0)');
                    }
                }
            }
        },
        scrollToAnchor() {
            let aTag = $("html");
            $('html,body').animate({scrollTop: aTag.offset().top}, 'slow');
        },
        clearAll() {
            $.ajax({
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                url: '/clear_filters/',
                data: {},
                dataType: 'json',
                type: 'POST',
                success: function (data) {
                    app._data.fcategory1 = [];
                    app._data.fcategory2 = [];
                    app._data.fcategory3 = [];
                    app._data.fbrand = [];
                    app._data.mfgroup = [];
                    app._data.mfcategory1 = [];
                    app._data.mfcategory2 = [];
                    app._data.mfcategory3 = [];
                    app._data.mfbrand = [];
                    app._data.mtxtsearch = "";
                    if (app._data.filterchips.length > 0) {
                        app._data.filterchips = [];
                    }
                    loadPage(1, 0);
                }
            });
        },
        callFilters() {
            app.filters = 1;
            app.page = 1;
            app._data.dialogfilter = false;
            loadPage(1, 0);
        },
        selectCatalog(folder) {
            app._data.dialogCatalogsModel = false;

            $.ajax({
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                url: '/set_catalog/',
                data: {
                    catalog: folder
                },
                dataType: 'json',
                type: 'POST',
                success: function (data) {
                    location.href = "/";
                }
            })
        },
        starClick(clusterId, itemIndex) {
            setRowMain(clusterId, itemIndex);
        },
        commentClick(clusterId, itemIndex) {
            getComment(clusterId, itemIndex);
        },
        wrongClick(clusterId, itemIndex) {
            setWrong(clusterId, itemIndex);
        },
        openCatalog() {
            this.dialogCatalogsModel = true;
        },
        login() {
            if (this.$refs.form.validate()) {
                app._data.errorLogin = "";
                app._data.errorAlert = false;

                let user = this.userModel;
                let password = this.passwordModel;

                $.ajax({
                    headers: {"X-CSRFToken": getCookie("csrftoken")},
                    url: '/user_login/',
                    data: {
                        user_name: user,
                        pass_word: password
                    },
                    dataType: 'json',
                    type: 'POST',
                    success: function (data) {
                        if (data['retorno'] == "ok") {
                            location.href = '/';
                        } else {
                            if (data['retorno'] == "error1") {
                                app._data.errorLogin = data['message'];
                                app._data.errorAlert = true;
                            } else {
                                app._data.errorLogin = data['message'];
                                app._data.errorAlert = true;
                            }
                        }
                    }
                });
            }
        },
        testebq() {
            $.ajax({
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                url: '/testebq/',
                data: {},
                dataType: 'json',
                type: 'POST',
                success: function (data) {
                    //console.log(data);
                }
            });
        },
        processCatalog() {
            $.ajax({
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                url: '/schedule_process/',
                data: {},
                dataType: 'json',
                type: 'POST',
                success: function (data) {
                    if (data['retorno'] == "Done") {
                        app._data.dialogProcessStarted = true;
                    }
                }
            });
        },
        publishCatalog() {
            $.ajax({
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                url: '/publish_catalog/',
                data: {},
                dataType: 'json',
                type: 'POST',
                success: function (data) {
                    //console.log(data);
                }
            });
        },
    },
});


// ----------------------------
// Data Explorer
// ----------------------------

function loadPage(isfilter = 0, callPage = 0) {
    let c1 = [];
    let c2 = [];
    let c3 = [];
    let b = [];
    let g = [];

    //c1.push(app._data.mfcategory1['value']);

    $.each(app._data.mfcategory1, function (key, val) {
        if (key == "value") {
            c1.push(val);
        }
    });
    $.each(app._data.mfcategory2, function (key2, val2) {
        if (key2 == "value") {
            c2.push(val2);
        }
    });
    $.each(app._data.mfcategory3, function (key3, val3) {
        if (key3 == "value") {
            c3.push(val3);
        }
    });
    $.each(app._data.mfbrand, function (key4, val4) {
        if (key4 == "value") {
            b.push(val4);
        }
    });
    $.each(app._data.mfgroup, function (key5, val5) {
        if (key5 == "value") {
            g.push(val5);
        }
    });

    let txt = app._data.mtxtsearch;

    let filters = "";

    filters += c1.length > 0 ? '&c1=' + c1 : "";
    filters += c2.length > 0 ? '&c2=' + c2 : "";
    filters += c3.length > 0 ? '&c3=' + c3 : "";
    filters += b.length > 0 ? '&b=' + b : "";
    filters += g.length > 0 ? '&g=' + g : "";
    filters += txt.length > 0 ? '&txt=' + txt : "";

    if (callPage > 0) {
        _page_index = callPage;
    }

    if (isfilter == 1 & (c1.length + c2.length + c3.length + b.length + g.length + txt.length) > 0) {
        _page_index = 1;

        app._data.items = [];
        app._data.dialogfilter = false;
        app._data.filterchips.length = 0;

        $.each(app._data.mfcategory1, function (key, val) {
            app._data.filterchips.push(val);
        });
        $.each(app._data.mfcategory2, function (key, val) {
            app._data.filterchips.push(val);
        });
        $.each(app._data.mfcategory3, function (key, val) {
            app._data.filterchips.push(val);
        });
        $.each(app._data.mfbrand, function (key, val) {
            app._data.filterchips.push(val);
        });
        $.each(app._data.mfgroup, function (key, val) {
            app._data.filterchips.push(val);
        });

        if (txt.length > 0) {
            app._data.filterchips.push(txt);
        }
    } else if (isfilter == 1 & (c1.length + c2.length + c3.length + b.length + g.length + txt.length) == 0) {
        _page_index = 1;

        filters += '&ini=1';
        app._data.items = [];
        app._data.dialogfilter = false;
    }

    $.getJSON("page_cluster?page=" + _page_index + filters, function (data) {
        app._data.items = [];
        app._data.headers = [];

        $.each(data.data, function (key, val) {
            app._data.items.push(val);
        });
        $.each(data.headers, function (key, val) {
            app._data.headers.push(val);
        });
		app.pages = data.total_record_num;
    });

    app.filters = 0;

    return false;
}

let filters = [];

function sortData(a, b) {
    if (a.item < b.item) {
        return -1;
    } else if (a.item > b.item) {
        return 1;
    } else {
        return 0;
    }
};

function setRowMain(clusterId, itemIndex) {
    $.ajax({
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        url: '/set_row_main/',
        data: {
            cluster_id: clusterId,
            item_index: itemIndex
        },
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            loadPage(this.filters, this.page);
        }
    });
}

function getComment(clusterId, itemIndex) {
    $.ajax({
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        url: '/get_comment/',
        data: {
            cluster_id: clusterId,
            item_index: itemIndex
        },
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            app._data.selectedItemModel = itemIndex;
            app._data.inputCommentModel = data['retorno'];
            app._data.dialogComment = true;
        }
    });
}

function setComment() {
    let itemIndex = app._data.selectedItemModel;
    let commentText = app._data.inputCommentModel;

    $.ajax({
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        url: '/set_comment/',
        data: {
            item_index: itemIndex,
            comment_text: commentText
        },
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            app._data.selectedItemModel = "";
            app._data.inputCommentModel = "";
            app._data.dialogComment = false;
            loadPage(this.filters, this.page);
        }
    });
}

function setWrong(clusterId, itemIndex) {
    $.ajax({
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        url: '/set_wrong/',
        data: {
            cluster_id: clusterId,
            item_index: itemIndex
        },
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            loadPage(this.filters, this.page);
        }
    });
}

function listFilters(element) {
    filters = [];
    $.getJSON("filters", function (data) {
        $.each(data, function (key, val) {
            filters.push(val);
        });

        switch (element) {
            case "":
                $.each(filters[4], function (key, val) {
                    if (key != "filter") {
                        app._data.fgroup.push(val);
                    }
                });
                app._data.fgroup = app._data.fgroup[0].sort(sortData);

                break;
            case "mfgroup":
                app._data.fcategory1 = [];

                $.each(filters[0], function (key, val) {
                    if (key != "filter") {
                        app._data.fcategory1.push(val);
                    }
                });
                app._data.fcategory1 = app._data.fcategory1[0].sort(sortData);

                break;
            case "mfcategory1":
                app._data.fcategory2 = [];

                $.each(filters[1], function (key, val) {
                    if (key != "filter") {
                        app._data.fcategory2.push(val);
                    }
                });
                app._data.fcategory2 = app._data.fcategory2[0].sort(sortData);

                break;
            case "mfcategory2":
                app._data.fcategory3 = [];

                $.each(filters[2], function (key, val) {
                    if (key != "filter") {
                        app._data.fcategory3.push(val);
                    }
                });
                app._data.fcategory3 = app._data.fcategory3[0].sort(sortData);

                break;
            case "mfcategory3":
                app._data.fbrand = [];

                $.each(filters[3], function (key, val) {
                    if (key != "filter") {
                        app._data.fbrand.push(val);
                    }
                });
                app._data.fbrand = app._data.fbrand[0].sort(sortData);

                break;
        }
    });

}

function setFilter(element, json_data) {
    if (json_data != "") {
        $.ajax({
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            url: '/set_filter/',
            data: {
                element: element,
                json_data: JSON.stringify(json_data)
            },
            dataType: 'json',
            type: 'POST'
        });

        //clear the filter arrays
        switch (element) {
            case "mfgroup":
                app._data.fcategory1 = [];
                app._data.fcategory2 = [];
                app._data.fcategory3 = [];
                app._data.fbrand = [];
                app._data.mfcategory1 = [];
                app._data.mfcategory2 = [];
                app._data.mfcategory3 = [];
                app._data.mfbrand = [];

                break;
            case "mfcategory1":
                app._data.fcategory2 = [];
                app._data.fcategory3 = [];
                app._data.fbrand = [];
                app._data.mfcategory2 = [];
                app._data.mfcategory3 = [];
                app._data.mfbrand = [];

                break;
            case "mfcategory2":
                app._data.fcategory3 = [];
                app._data.fbrand = [];
                app._data.mfcategory3 = [];
                app._data.mfbrand = [];

                break;
            case "mfcategory3":
                app._data.fbrand = [];
                app._data.mfbrand = [];

                break;
            case "mfbrand":
                break;
        }

        // Dynamic refresh (add items filtered)
        listFilters(element);
    }
}

function listQuantityPerPage() {
    $.getJSON("quantity_per_page", function (data) {
        $.each(data, function (key, val) {
            app._data.itemsquantitypage.push(val);
        });
    });
}

function setQuantityPerPage(qtde) {
    $.ajax({
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        url: '/set_quantity_per_page/',
        data: {
            quantity: qtde
        },
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            loadPage(0);
        }
    });
}

//function verifyJobEnd() {
//    //console.log("verifying job end...");
//    $.ajax({
//        headers: {"X-CSRFToken": getCookie("csrftoken")},
//        url: '/process_catalog_finished/',
//        data: {},
//        dataType: 'json',
//        type: 'POST',
//        beforeSend: function () {
//            app._data.loading = false;
//            app._data.dialogloading = false;
//        },
//        success: function (data) {
//            if (data['return_data'] == "Done") {
//                app._data.dialogProcessFinished = true;
//            }
//        }
//    });
//}

// ----------------------------
// Util
// ----------------------------

/* Work until page loads (including dataframes) */
$(document).ready().ajaxStart(function () {
    app._data.loading = true;
    app._data.dialogloading = true;
});

$(document).ready().ajaxComplete(function () {
    app._data.loading = false;
    app._data.dialogloading = false;
});

// window.setInterval(function(){
//     verifyJobEnd();
// }, 15000);

$(document).ready(function () {
    $("#feedpage").hide();

    // (function () {
    //     setTimeout(verifyJobEnd(), 15000);
    // })();

    app.filters = 1;
    app.page = 1;

    listQuantityPerPage();
    listFilters("");
});

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

function watchEnter() {
    if (app._data.rightDrawer == true) {
        app.callFilters();
    }
}

function watchEsc() {
    app._data.rightDrawer = !app._data.rightDrawer;
}

function getCatalogStatus() {
    $.getJSON("get_catalog_info", function (data) {
        app._data.catalogInfo = data;
        app._data.canProcess = data["canProcess"];
        app._data.canPublish = data["canPublish"];
    });
}

function graph() {
    var d3 = Plotly.d3;
    var WIDTH_IN_PERCENT_OF_PARENT = 90,
        HEIGHT_IN_PERCENT_OF_PARENT = 90;

    var gd3 = d3.select("div[id='graph-element']")
        .style({
            width: WIDTH_IN_PERCENT_OF_PARENT + '%',
            'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',

            height: HEIGHT_IN_PERCENT_OF_PARENT + 'vh',
            'margin-top': (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + 'vh'
        });

    var my_div = gd3.node();

    window.onresize = function () {
        Plotly.Plots.resize(my_div);
    };

    Plotly.d3.csv('https://raw.githubusercontent.com/plotly/datasets/master/3d-scatter.csv', function (err, rows) {
        function unpack(rows, key) {
            return rows.map(function (row) {
                return row[key];
            });
        }

        var trace1 = {
            x: unpack(rows, 'x1'), y: unpack(rows, 'y1'), z: unpack(rows, 'z1'),
            mode: 'markers',
            marker: {
                size: 12,
                line: {
                    color: 'rgba(217, 217, 217, 0.14)',
                    width: 0.5
                },
                opacity: 0.8
            },
            type: 'scatter3d'
        };
        /*
                var trace2 = {
                    x: unpack(rows, 'x2'), y: unpack(rows, 'y2'), z: unpack(rows, 'z2'),
                    mode: 'markers',
                    marker: {
                        color: 'rgb(127, 127, 127)',
                        size: 12,
                        symbol: 'circle',
                        line: {
                            color: 'rgb(204, 204, 204)',
                            width: 1
                        },
                        opacity: 0.9
                    },
                    type: 'scatter3d'
                };

                var data = [trace1, trace2];
        */
        var data = [trace1];

        Plotly.plot(my_div, data);
    });
}
