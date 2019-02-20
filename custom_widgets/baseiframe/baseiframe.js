function baseiframe(widget_id, url, skin, parameters)
{
    self = this
    // Initialization
    
    self.parameters = parameters;
    
    var callbacks = []

    if ("camera" in self.parameters)
    {
        self.set_camera = set_camera
        var monitored_entities = 
            [
                {"entity": parameters.camera, "initial": self.set_camera, "update": self.set_camera}
            ]    
    }
    else
    {
        var monitored_entities = []    
    }
   
    // Call the parent constructor to get things moving
    
    WidgetBase.call(self, widget_id, url, skin, parameters, monitored_entities, callbacks);

    // Set the url
    
    if ("url_list" in parameters || "img_list" in parameters || "entity_picture" in parameters)
    {
        self.index = 0;
        refresh_frame(self,"");
    }
    
    
    function refresh_frame(self)
    {
        if ("url_list" in self.parameters)
        {
            self.set_field(self, "frame_src", self.parameters.url_list[self.index]);
            self.set_field(self, "img_src", "/images/Blank.gif");
            size = self.parameters.url_list.length;
        }
        else if ("img_list" in self.parameters)
        {
            var url = self.parameters.img_list[self.index];
            if (url.indexOf('?') > -1)
            {
                url = url + "&time=" + Math.floor((new Date).getTime()/1000);
            }
            else
            {
                url = url + "?time=" + Math.floor((new Date).getTime()/1000);
            }
            self.set_field(self, "img_src", url);
            size = self.parameters.img_list.length;
        }
        else if ("entity_picture" in self.parameters)
        {
            var url = self.parameters.entity_picture;
            if (url.indexOf('?') > -1)
            {
                url = url + "&time=" + Math.floor((new Date).getTime()/1000);
            }
            else
            {
                url = url + "?time=" + Math.floor((new Date).getTime()/1000);
            }
            self.set_field(self, "img_src", url);
            size = 1
        }
       
        if ("refresh" in self.parameters)
        {
            self.index = self.index + 1;
            if (self.index == size)
            {
                self.index = 0;
            }
            setTimeout(function() {refresh_frame(self)}, self.parameters.refresh * 1000);
        }
    }
    function set_camera(self,state)
    {
        self.state = state.state;
        url_part1 = self.parameters.ha_url;
        url_part2 = state.attributes.entity_picture;
        url_part3 = "";
        if ("password" in self.parameters)
        {
            url_part3 = "&api_password=" + self.parameters.password;
        }
        if ("token" in self.parameters)
        {
            url_part2 =  "/api/camera_proxy_stream/"+ self.parameters.camera
            url_part3 = "?token=" + self.parameters.token;
        }
        url = url_part1 + url_part2 + url_part3;
        view_camera(self, url)
    }
    function view_camera(self,url)
    {
        changingurl = url + "&time=" + Math.floor((new Date).getTime()/1000);
        self.set_field(self, "img_src", changingurl);
        if ("refresh" in self.parameters)
        {
            refreshrate = self.parameters.refresh
        }
        else
        {    
            refreshrate = 10
        }
        
        setTimeout(function() {view_camera(self, url)}, refreshrate * 1000);
    }
}
