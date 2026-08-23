const notificationConfigElement = document.getElementById("notification-manager-config");
const userId = notificationConfigElement?.dataset.userId;
const csrfToken = notificationConfigElement?.dataset.csrfToken;
const notificationsChannelPrefix = notificationConfigElement?.dataset.channelPrefix;
const getNotificationsUrl = notificationConfigElement?.dataset.notificationsUrl;

class NotificationManager {
    constructor() {
        this.eventSource = null;
        this.elements = {};
        this.state = {
            newNotificationIds: [],
            hasMore: true,
            page: 1,
            isLoading: false
        };
        this.config = {
            getNotificationsUrl: getNotificationsUrl,
            eventSourceUrl: `/events/${notificationsChannelPrefix}${userId}/`,
            reconnectInterval: 5000,
            maxReconnectAttempts: 10
        };
        this.reconnectAttempts = 0;

        // handler refs will be created when we set up listeners
        this._onLoadMoreClick = null;
        this._onReadAllClick = null;

        this.init();
    }

    init() {
        this.cacheElements();
        this.setupEventListeners();
        this.createEventSource();
        this.loadNotifications();
    }

    cacheElements() {
        this.elements = {
            notificationList: document.getElementById("notification-list"),
            emptyNotification: document.getElementById("empty-notification"),
            loadMoreButton: document.getElementById("load-notifications-button"),
            notificationsContainerFooter: document.getElementById("notifications-container-footer"),
            notificationCount: document.getElementById("notification-count"),
            readAllNotificationsButton: document.getElementById("read-all-notifications-button"),
        };

        // Validate required elements
        const requiredElements = ["notificationList", "emptyNotification", "loadMoreButton", "readAllNotificationsButton"];
        for (const elementName of requiredElements) {
            if (!this.elements[elementName]) {
                console.error(`Required element not found: ${elementName}`);
            }
        }
    }

    setupEventListeners() {
        // Window beforeunload event
        window.addEventListener("beforeunload", () => {
            this.closeEventSource();
        });

        // Load more button
        if (this.elements.loadMoreButton) {
            this._onLoadMoreClick = (event) => {
                event.preventDefault();
                this.loadMoreNotifications();
            };
            this.elements.loadMoreButton.addEventListener("click", this._onLoadMoreClick);
        }

        if (this.elements.readAllNotificationsButton) {
            this._onReadAllClick = (event) => {
                event.preventDefault();
                this.readAllNotifications();
            };
            this.elements.readAllNotificationsButton.addEventListener("click", this._onReadAllClick);
        }

        // Page visibility change (to reconnect when tab becomes active)
        document.addEventListener("visibilitychange", () => {
            if (!document.hidden && (!this.eventSource || this.eventSource.readyState === EventSource.CLOSED)) {
                this.createEventSource();
            }
        });
    }

    createEventSource() {
        this.closeEventSource();

        try {
            // Use ReconnectingEventSource if available, otherwise fallback to EventSource
            const EventSourceClass = window.ReconnectingEventSource || EventSource;
            this.eventSource = new EventSourceClass(this.config.eventSourceUrl);

            this.eventSource.addEventListener("open", () => {
                console.log("EventSource connection opened");
                this.reconnectAttempts = 0;
            });

            this.eventSource.addEventListener("message", (event) => {
                this.handleNewNotification(event);
            });

            this.eventSource.addEventListener("notification_read", (event) => {
                this.handleNotificationRead(event);
            });

            this.eventSource.addEventListener("all_notifications_read", (event) => {
                this.handleAllNotificationsRead(event);
            });

            this.eventSource.addEventListener("error", (event) => {
                this.handleEventSourceError(event);
            });

        } catch (error) {
            console.error("Failed to create EventSource:", error);
            this.scheduleReconnect();
        }
    }

    closeEventSource() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }

    handleEventSourceError(event) {
        console.error("EventSource error:", event);

        if (this.reconnectAttempts < this.config.maxReconnectAttempts) {
            this.scheduleReconnect();
        } else {
            console.error("Max reconnection attempts reached");
        }
    }

    scheduleReconnect() {
        this.reconnectAttempts++;
        console.log(`Scheduling reconnect attempt ${this.reconnectAttempts}`);

        setTimeout(() => {
            if (!this.eventSource || this.eventSource.readyState === EventSource.CLOSED) {
                this.createEventSource();
            }
        }, this.config.reconnectInterval);
    }

    updateNotificationCount(data) {
        if (!this.elements.notificationCount) return;

        const count = data.count || 0;
        this.elements.notificationCount.textContent = count;
        this.elements.notificationCount.style.display = count > 0 ? "inline-block" : "none";

        if (this.elements.readAllNotificationsButton) {
            this.elements.readAllNotificationsButton.style.display = count > 0 ? "inline-block" : "none";
            this.elements.readAllNotificationsButton.disabled = this.state.isLoading;
        }

        if (this.elements.emptyNotification) {
            this.elements.emptyNotification.style.display = count > 0 ? "none" : "block";
        }
    }

    async makeRequest(url, options = {}) {
        const defaultOptions = {
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            }
        };

        const mergedOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, mergedOptions);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Request failed:", error);
            throw error;
        }
    }

    async getNotifications() {
        if (this.state.isLoading) {
            return null;
        }

        this.state.isLoading = true;

        try {
            const data = await this.makeRequest(this.config.getNotificationsUrl, {
                method: "POST",
                body: JSON.stringify({
                    page: this.state.page,
                    new_notification_ids: this.state.newNotificationIds
                })
            });

            this.state.page++;
            return data;
        } catch (error) {
            console.error("Error loading notifications:", error);
            return null;
        } finally {
            this.state.isLoading = false;
        }
    }

    createNotificationElement(html) {
        const container = document.createElement("div");
        container.innerHTML = html.trim();
        return container.firstElementChild;
    }

    renderNotifications(notificationsHtml, append = false) {
        if (!this.elements.notificationList) return;

        if (!append) {
            this.elements.notificationList.innerHTML = "";
        }

        if (notificationsHtml && notificationsHtml.length > 0) {
            const fragment = document.createDocumentFragment();

            notificationsHtml.forEach(html => {
                const notificationElement = this.createNotificationElement(html);
                if (notificationElement) {
                    fragment.appendChild(notificationElement);
                }
            });

            this.elements.notificationList.appendChild(fragment);
        }
    }

    updateNotificationButtons(data) {
        if (this.elements.loadMoreButton) {
            this.elements.loadMoreButton.style.display = this.state.hasMore ? "inline-block" : "none";
            this.elements.loadMoreButton.disabled = this.state.isLoading;
        }

        if (this.elements.readAllNotificationsButton) {
            this.elements.readAllNotificationsButton.style.display = data.count > 0 ? "inline-block" : "none";
            this.elements.readAllNotificationsButton.disabled = this.state.isLoading;
        }

        if (this.elements.notificationsContainerFooter && this.areNotificationButtonsHidden()) {
            this.elements.notificationsContainerFooter.style.display = this.state.hasMore ? "block" : "none";
        }
    }

    areNotificationButtonsHidden() {
        return this.elements.loadMoreButton.style.display === "none" && this.elements.readAllNotificationsButton.style.display === "none";
    }

    async loadNotifications() {
        try {
            const data = await this.getNotifications();
            if (!data) return;

            this.updateNotificationCount(data);
            this.renderNotifications(data.notifications_html, false);
            this.state.hasMore = data.has_next || false;
            this.updateNotificationButtons(data);
        } catch (error) {
            console.error("Failed to load notifications:", error);
        }
    }

    async loadMoreNotifications() {
        if (!this.state.hasMore || this.state.isLoading) return;

        try {
            const data = await this.getNotifications();
            if (!data) return;

            this.renderNotifications(data.notifications_html, true);
            this.state.hasMore = data.has_next || false;
            this.updateNotificationButtons(data);
        } catch (error) {
            console.error("Failed to load more notifications:", error);
        }
    }

    async readAllNotifications(evt) {
        await this.makeRequest(`${getNotificationsUrl}`, {
            method: "PATCH",
        });
    }

    handleNewNotification(event) {
        try {
            const data = JSON.parse(event.data);
            this.updateNotificationCount(data);

            if (data.notification_html) {
                const newNotificationElement = this.createNotificationElement(data.notification_html);

                if (newNotificationElement && this.elements.notificationList) {
                    // Extract notification ID and add to tracking array
                    const notificationId = newNotificationElement.id;
                    if (notificationId) {
                        const idMatch = notificationId.match(/notification-(\d+)/);
                        if (idMatch) {
                            this.state.newNotificationIds.push(parseInt(idMatch[1]));
                        }
                    }

                    this.elements.notificationList.prepend(newNotificationElement);

                    if (this.elements.emptyNotification) {
                        this.elements.emptyNotification.style.display = "none";
                    }
                }
            }
        } catch (error) {
            console.error("Error handling new notification:", error);
        }
    }

    handleNotificationRead(event) {
        try {
            const data = JSON.parse(event.data);
            const notificationElement = document.getElementById(`notification-${data.notification_id}`);

            if (notificationElement) {
                notificationElement.remove();
                this.updateNotificationCount(data);
            }
        } catch (error) {
            console.error("Error handling notification read:", error);
        }
    }

    handleAllNotificationsRead(event) {
        try {
            const data = JSON.parse(event.data);

            this.state.hasMore = false;
            this.elements.notificationList.innerHTML = "";
            this.updateNotificationCount(data);
            this.updateNotificationButtons(data);
        } catch (error) {
            console.error("Error handling notification read:", error);
        }
    }

    // Public methods for external use
    refresh() {
        this.state.page = 1;
        this.state.newNotificationIds = [];
        this.loadNotifications();
    }

    destroy() {
        this.closeEventSource();
        // Remove event listeners if needed
        if (this.elements.loadMoreButton) {
            this.elements.loadMoreButton.removeEventListener("click", this._onLoadMoreClick);
        }

        if (this.elements.readAllNotificationsButton) {
            this.elements.readAllNotificationsButton.removeEventListener("click", this._onReadAllClick);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
    if (!notificationConfigElement) {
        return;
    }

    // Initialize the notification manager
    window.notificationManager = new NotificationManager();
});


// Global function for notifications click events
function readNotification(notificationId) {
    fetch(`${getNotificationsUrl}/${notificationId}`, {
        method: "PATCH",
        headers: {
            "X-CSRFToken": csrfToken,
        },
    }).catch(error => console.error("Error:", error));
}
