
openerp.web_chat = function(instance) {

    instance.web.UserMenu.include({
        do_update: function(){
            var self = this;
            this.update_promise.then(function() {
                var chat = new instance.web_chat.Chat(self);
                chat.appendTo(instance.client.$el);
                var button = new instance.web.ChatTopButton(self);
                button.chat = chat;
                button.appendTo(instance.webclient.$el.find('.oe_systray'));
            });
            return this._super.apply(this, arguments);
        },
    });

    instance.web.ChatTopButton = instance.web.Widget.extend({
        template:'ChatTopButton',
        events: {
            "click button": "clicked",
        },
        clicked: function() {
            this.chat.switch_display();
        },
    });

    instance.web_chat.Chat = instance.web.Widget.extend({
        template: "Chat",
        init: function(parent) {
            this._super(parent);
            this.shown = false;
        },
        start: function() {
            var self = this;
            this.$el.css("right", -this.$el.outerWidth());
            self.poll();
            self.last = null;
            $(window).scroll(_.bind(this.calc_box, this));
            $(window).resize(_.bind(this.calc_box, this));
            self.calc_box();
            self.$(".oe_chat_input").keypress(function(e) {
                if(e.which != 13) {
                    return;
                }
                var mes = self.$(".oe_chat_input").val();
                self.$(".oe_chat_input").val("");
                var model = new instance.web.Model("chat.message");
                model.call("post", [mes], {context: new instance.web.CompoundContext()});
            }).focus();
        },
        calc_box: function() {
            var $topbar = instance.client.$(".oe_topbar");
            var top = $topbar.offset().top + $topbar.height();
            top = Math.max(top - $(window).scrollTop(), 0);
            this.$el.css("top", top);
            this.$el.css("bottom", 0);
        },
        switch_display: function() {
            if (this.shown) {
                this.$el.animate({
                    right: -this.$el.outerWidth(),
                });
            } else {
                this.$el.animate({
                    right: 0,
                });
            }
            this.shown = ! this.shown;
        },
        poll: function() {
            var self = this;
            this.rpc("/chat/poll", {
                last: this.last,
                context: new instance.web.CompoundContext()
            }, {shadow: true}).then(function(result) {
                self.last = result.last;
                _.each(result.res, function(mes) {
                    $("<div>").text(mes).appendTo(self.$(".oe_chat_content"));
                });
                self.poll();
            }, function(unused, e) {
                e.preventDefault();
                setTimeout(_.bind(self.poll, self), 5000);
            });
        }
    });

}