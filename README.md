Main: [![Build Status](https://travis-ci.com/uva-cs3240-s21/project-a-02.svg?token=qjZb3t7Jyo2qjf2ZnRYF&branch=main)](https://travis-ci.com/uva-cs3240-s21/project-a-02)

# Final Project for group A-02
This is a map of the UVA campus ("Grounds") built using Django, Travis CI, and Heroku. It
is designed to fulfill the requirements set out in Spring 2021 CS 3240. 

Features in this project include a user being able to create an event that other users can attend, 
find buildings and classes on an interactive map, navigate from one building to another, and create
schedules for classes. 

The schedule and finding building functionality is on the tab schedule. The page that the user is currently on
is bolded in the navigation bar. The classes can be searched by the title of the course or the class mnemonic with
a space between the course number in the search bar. Buildings can be searched by name in the search bar. Classes can
be added by clicking the add class and shown on the map by clicking the show on map button. The classes can be seen after 
clicking the button labeled my classes at the top. Markers on the map can be right clicked which removes it, and left clicking
on it will reveal some details on it. Classes under the my classes button can be removed using the remove button. The features
involving classes need the user to be logged in to work/show.

Events can be created by clicking the create events button on the event page. An event has a title, host, time, date, and 
description. A user that created an event can update the event at a later time, as long as the event as not expired. The user
that is the host can also cancel the event. Events will expire automatically once the event has started, so no other users can
join once it has started. Events can be viewed by clicking the events button on the events page. A list of events will be shown
with the titles and buttons for details, whether to attend/don't attend or cancel, and update, depending on whether the user is
a host or an attendee. All of these features require the user to be logged in.

NOTICE: Mapbox API for some building will place a marker in the wrong place or not be able to find the given building.

Copyright <2021> <Justin Liu, Eli Jelesko, Alejandro Perera, Zack Yahn, David Chen>

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Copyright [2021] <Justin Liu, Eli Jelesko, Alejandro Perera, Zach Yahn, David Chen>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

The UI used bootswatch in order to make it feel different from the usual bootstrap. The theme is darkly.css. Copyright are 
darkly.css file.
