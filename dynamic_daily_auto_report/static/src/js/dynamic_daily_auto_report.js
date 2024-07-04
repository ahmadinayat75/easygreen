odoo.define('dynamic_daily_auto_report.custom_script_extension', function (require) {
    "use strict";

var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');
    var Data = require('web.DataExport');
    Data.include({
        _showExportsList: function () {
        var model = this.record.model;

        var args = [model];
        console.log(args);
        var self = this;
        if (this.$('.o_exported_lists_select').is(':hidden')) {
            this.$('.o_exported_lists').show();
            return Promise.resolve();
        }

        return rpc.query({
            model: 'ir.exports',
            method: 'get_user_list',
            args: [model]
        }).then(function (exportList) {
            self.$('.o_exported_lists').append(QWeb.render('Export.SavedList', {
                existing_exports: exportList,
            }));
        });
    },

    });
});
