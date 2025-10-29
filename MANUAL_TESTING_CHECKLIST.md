# Manual Testing Checklist

## Authentication Removal Tests

### ✅ Page Access Without Profile
- [ ] Open app without creating profile - should show main page
- [ ] Navigate to Ana Sayfa - should work without profile
- [ ] Navigate to Dersler - should work without profile
- [ ] Navigate to Ödevler - should work without profile
- [ ] Navigate to Takvim - should work without profile
- [ ] Navigate to Hatırlatıcılar - should work without profile
- [ ] Navigate to Not Ortalaması - should work without profile
- [ ] Navigate to Profil - should show profile creation form

### ✅ Profile Display
- [ ] Sidebar shows "Profil oluşturmak için..." when no profile exists
- [ ] Create profile from Profil page
- [ ] Sidebar shows profile info after creation
- [ ] Profile info displays correctly (name, email, student ID, department)

## Input Validation Tests

### ✅ Course Form Validation

**Invalid Inputs (should show errors):**
- [ ] Course name: "A" → Error: "en az 2 karakter"
- [ ] Course name: Empty → Error: "boş bırakılamaz"
- [ ] Course code: "A" → Error: "en az 2 karakter"
- [ ] Course code: "CS@201" → Error: "harf, rakam, boşluk ve tire"
- [ ] Start time: 10:30, End time: 09:00 → Error: "Başlangıç saati bitiş saatinden önce"
- [ ] Start time: 09:00, End time: 09:20 → Error: "en az 30 dakika"
- [ ] Credits: 0 → Error: "1-15 arasında"
- [ ] Credits: 20 → Error: "1-15 arasında"

**Valid Inputs (should succeed):**
- [ ] Course name: "Veri Yapıları"
- [ ] Course code: "CS201"
- [ ] Start time: 09:00, End time: 10:30
- [ ] Credits: 3
- [ ] Form submits successfully
- [ ] Course appears in list

### ✅ Assignment Form Validation

**Invalid Inputs (should show errors):**
- [ ] Title: "HW" → Error: "en az 3 karakter"
- [ ] Title: (250 characters) → Error: "en fazla 200 karakter"
- [ ] Description: (2500 characters) → Error: "en fazla 2000 karakter"
- [ ] Due date: 3 years in future → Error: "2 yıldan fazla ileri"
- [ ] Type: Invalid → Error: "Geçersiz görev türü"
- [ ] Priority: Invalid → Error: "Geçersiz öncelik"

**Valid Inputs (should succeed):**
- [ ] Title: "Ödev 1"
- [ ] Description: "Alıştırmaları tamamla"
- [ ] Type: Ödev
- [ ] Due date: Next week
- [ ] Priority: Orta
- [ ] Form submits successfully
- [ ] Assignment appears in list

**Warning (should show warning but allow submission):**
- [ ] Due date: Yesterday → Warning: "geçmişte" but allows submission
- [ ] Assignment is created despite warning

### ✅ Grade Form Validation

**Invalid Inputs (should show errors):**
- [ ] Grade: -0.5 → Error: "0.0-4.0 arasında"
- [ ] Grade: 4.5 → Error: "0.0-4.0 arasında"
- [ ] Credits: 0 → Error: "1-15 arasında"
- [ ] Credits: 20 → Error: "1-15 arasında"

**Valid Inputs (should succeed):**
- [ ] Course name: "Veri Yapıları"
- [ ] Grade: 3.5
- [ ] Credits: 3
- [ ] Semester: Güz
- [ ] Year: 2024
- [ ] Form submits successfully
- [ ] Grade appears in list
- [ ] GPA is calculated correctly

### ✅ Profile Form Validation

**Invalid Inputs (should show errors):**
- [ ] Name: "A" → Error: "en az 2 karakter"
- [ ] Name: Empty → Error: "boş bırakılamaz"
- [ ] Email: "invalid" → Error: "Geçerli bir e-posta"
- [ ] Email: Empty → Error: "E-posta boş bırakılamaz"
- [ ] Student ID: "2020-123456" → Error: "sadece harf ve rakam"
- [ ] Student ID: (25 characters) → Error: "en fazla 20 karakter"
- [ ] Class year: 10 → Error: "1-8 arasında"

**Valid Inputs (should succeed):**
- [ ] Name: "Ahmet Yılmaz"
- [ ] Email: "ahmet@universite.edu.tr"
- [ ] Student ID: "2020123456"
- [ ] Department: "Bilgisayar Mühendisliği"
- [ ] Class year: 3
- [ ] Form submits successfully
- [ ] Profile is created/updated
- [ ] Profile displays in sidebar

## Form Data Preservation Tests

### ✅ Data Retention on Validation Failure
- [ ] Fill course form with invalid data
- [ ] Submit form
- [ ] Error message displays
- [ ] Form fields retain entered values (not cleared)
- [ ] Fix error and resubmit
- [ ] Form submits successfully

## Turkish Error Messages Tests

### ✅ Error Message Display
- [ ] All error messages display in Turkish
- [ ] Error messages include emoji icons (❌, ⚠️)
- [ ] Error messages are clear and specific
- [ ] Error messages suggest how to fix the issue

## Functionality Tests

### ✅ App Works Without Profile
- [ ] Add course without profile → Success
- [ ] Add assignment without profile → Success
- [ ] Add grade without profile → Success
- [ ] View dashboard without profile → Success
- [ ] All statistics display correctly
- [ ] No errors or crashes

### ✅ App Works With Profile
- [ ] Create profile
- [ ] Profile displays in sidebar
- [ ] Add course with profile → Success
- [ ] Add assignment with profile → Success
- [ ] Add grade with profile → Success
- [ ] All features work normally

## Edge Cases

### ✅ Boundary Values
- [ ] Course name: Exactly 2 characters → Success
- [ ] Course name: Exactly 100 characters → Success
- [ ] Assignment title: Exactly 3 characters → Success
- [ ] Assignment title: Exactly 200 characters → Success
- [ ] Grade: Exactly 0.0 → Success
- [ ] Grade: Exactly 4.0 → Success
- [ ] Credits: Exactly 1 → Success
- [ ] Credits: Exactly 15 → Success

### ✅ Special Characters
- [ ] Course code: "CS 201" (with space) → Success
- [ ] Course code: "CS-201" (with dash) → Success
- [ ] Email: "user.name@domain.com" → Success
- [ ] Email: "user+tag@domain.edu.tr" → Success

## Performance Tests

### ✅ Validation Speed
- [ ] Validation happens instantly (< 100ms)
- [ ] No noticeable delay when submitting forms
- [ ] Error messages appear immediately

## Summary

**Total Tests:** 80+
**Critical Tests:** 40
**Expected Result:** All tests should pass

**Notes:**
- All validation errors should be in Turkish
- All error messages should include emoji icons
- Form data should be preserved on validation failure
- App should work perfectly without profile
- No page should require profile to access
