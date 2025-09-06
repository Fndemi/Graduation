# Product Guide

This document explains how products are structured for catalog and chatbot understanding.

---

## Product Basics

- **Name**: Clear, descriptive product title.  
  Example: `"Luxury Sofa"`.

- **Description**: Short, meaningful explanation of use.  
  Example: `"A comfy sofa for your living room."`.

- **Category**: High-level grouping. Allowed examples: `Top Picks`, `Top Selling`, `Discounted`.

- **Niche**: Area or context of use. Examples: `living room`, `kitchen`, `bathroom`, `bedroom`.

---

## Pricing

- **Initial Price**: Original product price. Example: `30000`.
- **Discount Percent**: Reduction percentage. Normally 0–100%.  
  Example: `55%`.
- **Discounted Price**: Price after applying discount.  
  Formula: `discountedPrice = initialPrice - (initialPrice * discountPercent / 100)`  
  Example: `13500`.

---

## Media

- **Image URL**: Visual representation of product.  
  Example: `https://res.cloudinary.com/.../products/xcfhrkpkdunsyoi4w2mh.jpg`.

---

## User Feedback

- **Reviews**: Optional user opinions.  
  - **Comment**: Short text.  
  - **Rating**: Number 1–5.  

Example review: `"Awesome", rating 4`.

---

## Example Product

```json
{
  "name": "Premium Wooden Chair",
  "description": "A comfy chair for your living room.",
  "initialPrice": 50000,
  "discountPercent": 20,
  "discountedPrice": 40000,
  "category": "Top Picks",
  "niche": "living room",
  "image": "https://res.cloudinary.com/.../products/iyvefqdhmfbr5cwcbzga.jpg",
  "reviews": [
    {"comment": "The best of the best", "rating": 5}
  ]
}
