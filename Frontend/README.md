# Where is my Thief - Frontend [![version][version-badge]][CHANGELOG] [![license][license-badge]][LICENSE]

> This Application is derived from [Vue Light Bootstrap Dashboard](http://vuejs.creative-tim.com/vue-light-bootstrap-dashboard) and uses components such as [vue-leafet](#) for map rendering and [bootrap-vue](https://github.com/bootstrap-vue/bootstrap-vue) for layouting and such.

## :rocket: Getting started

Go to the Projects main main [README](../README.md) if you want to use the whole Ecosystem.

If you want to contribute for development on the Frontend side you may do the follwoing:
1. Clone the project
2. Make sure you have [node](https://nodejs.org/en/) installed
3. Type `npm install` in the source folder where `package.json` is located
4. Type `npm run dev` to start the development server

# Routes and Pages
The application contains follwoing views which are acceable over:

### User Pages
- `/users/login` : <br>
    Loginpage
- `/users/register` : <br>
    Registerpage
- `/users/{username}/overview` :<br>
    Mainpage where all your Registerd devices appear
- `/users/{username}/settings` :<br>
    This page sets up user settings and profile information

### Device Pages
- `/devices/{deviceid}/overview` : <br>
    Here are all infromations, status and location logic of your My Thief Device. There is also the logic for auqreing the configuration file for the Device when not fully setup to the Application
- `/devices/{deviceid}/settings` : <br>
    Here the user may change all Data of the device which are used wihtin our [API](#)


[CHANGELOG]: ./CHANGELOG.md
[LICENSE]: ./LICENSE.md
[version-badge]: https://img.shields.io/badge/version-1.0.0-blue.svg
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg
