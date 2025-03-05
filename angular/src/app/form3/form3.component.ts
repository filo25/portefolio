import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// https://v17.angular.io/guide/forms#building-a-template-driven-form
// https://angular.dev/guide/forms/form-validation

export class Hero {

  constructor(
    public id: number,
    public name: string,
    public power: string,
    public alterEgo?: string
  ) {}

}

@Component({
  selector: 'app-form3',
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './form3.component.html',
  styleUrl: './form3.component.scss'
})
export class Form3Component {

  powers = ['Really Smart', 'Super Flexible',
            'Super Hot', 'Weather Changer'];

  // this is what gets boundt in the html
  model = new Hero(18, 'Dr. IQ', this.powers[0], 'Chuck Overstreet');

  submitted = false;

  onSubmit() { this.submitted = true; }

}
