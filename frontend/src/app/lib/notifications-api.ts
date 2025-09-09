import { apiCall } from './auth';

export type Notification = {
  _id: string;
  userId: string;
  message: string;
  read: boolean;
  createdAt: string;
};

/**
 * Fetch notifications for a specific user using centralized API call
 */
export async function fetchNotifications(userId: string): Promise<Notification[]> {
  try {
    const data = await apiCall(`/notifications/user/${userId}`, {
      method: 'GET',
    });
    return data as Notification[]; // Type assertion
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to fetch notifications';
    throw new Error(errorMessage);
  }
}

/**
 * Mark a notification as read using centralized API call
 */
export async function markAsRead(id: string): Promise<void> {
  try {
    await apiCall(`/notifications/${id}`, {
      method: 'PATCH',
      body: JSON.stringify({ read: true }),
    });
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to mark as read';
    throw new Error(errorMessage);
  }
}

/**
 * Delete a notification using centralized API call
 */
export async function deleteNotification(id: string): Promise<void> {
  try {
    await apiCall(`/notifications/${id}`, {
      method: 'DELETE',
    });
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to delete notification';
    throw new Error(errorMessage);
  }
}
