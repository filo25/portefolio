import { Routes } from '@angular/router';

import { ApiComponent } from './api/api.component';
import { AsyncComponent } from './async/async.component';
//import { FormComponent } from './form/form.component';
//import { Form2Component } from './form2/form2.component';
import { Form3Component } from './form3/form3.component';
//import { Form4Component } from './form4/form4.component';
import { HomeComponent } from './home/home.component';
//import { PostComponent } from './post/post.component';
import { TableComponent } from './table/table.component';

export const routes: Routes = [
  { path: 'api', component: ApiComponent },
  { path: 'async', component: AsyncComponent },
  //{ path: 'form', component: FormComponent },
  //{ path: 'form2', component: Form2Component },
  { path: 'form3', component: Form3Component },
  //{ path: 'form4', component: Form4Component },
  { path: 'home', component: HomeComponent },
  //{ path: 'post', component: PostComponent },
  { path: 'table', component: TableComponent },
  { path: '**', component: HomeComponent }
];
