var Actions = {
    initialize: function() {
        console.log('Initialize Actions');
        this.setSlugAlbum();
        this.stylingUpdateAlbum();
    },

    setSlugAlbum : function (){
        let that = this;
        $('#id_title').keyup(function() {
            let str = $('#id_title').val();
            for (var i = 0; i < str.length; i++) {
               str = str.replace(" ", "-"); 
            }
            $('#id_slug').val(str.toLowerCase());
        });
    },

    stylingUpdateAlbum: function(){
        let that = this;
        $('form#album_update_form > p').addClass('form-group row');
        $('form#album_update_form > p > input[type="text"]').addClass('form-control');
        $('form#album_update_form > input[type="submit"]').addClass('btn btn-success');
    }

}

Actions.initialize();
