import angular from 'angular';

import _ from 'underscore';
import {nbv, DataBrowserService } from './data-browser-service';
import { DataService } from './data-service';
import { FileListing } from './file-listing';
import { LoggingServiceProvider } from './logging-service';
import { notificationFactory } from './notification-factory';
import { ProjectEntitiesService } from './project-entity-service';
import { ProjectService } from './project-service';
import { SystemsService } from './systems-service';
import { TicketsService } from './tickets-service';
import { UserService } from './user-service';

let designsafeServices = angular.module('designsafe.services', []);

designsafeServices.factory('nbv', ['$window', nbv]);
designsafeServices.factory('DataBrowserService', DataBrowserService);
designsafeServices.factory('DataService', DataService);
designsafeServices.factory('FileListing', ['$http', '$q', 'Logging', FileListing]);
designsafeServices.provider('Logging', LoggingServiceProvider);
designsafeServices.factory('notificationFactory', notificationFactory);
designsafeServices.factory('ProjectEntitiesService', ProjectEntitiesService);
designsafeServices.factory('ProjectService', ProjectService);
designsafeServices.factory('SystemsService', SystemsService);
designsafeServices.service('TicketsService', TicketsService);
designsafeServices.service('UserService', UserService);

export default designsafeServices;
